import tornado.web
import tornado.ioloop
import json
import numpy as np
from skopt import Optimizer
from datetime import datetime
from skopt import dump
from pandas import DataFrame
from keras.models import Sequential, load_model
from pandas import concat
import numpy
from keras.layers import Dense,LSTM,Bidirectional
from keras.layers import Flatten
from keras.layers.convolutional import Conv1D
from keras.layers.convolutional import MaxPooling1D
from numpy import array
from keras.layers import TimeDistributed
from keras.layers import RepeatVector
#定义真实采样数
gTotalNumber=0
#定义集群返回迭代数，当集群返回总数==真实采样数时，集群计算停止（sobo:5w轮）
gcount=0
#定义接收参数集：X，类型-列表
gX=[]
#定义接收结果集:Y，类型-列表
gY=[]
#定义问题参数空间，类型-字典
gproblem={}
gopt=None
gindex=[]
gmsgreturn=[]
gIter=0
gmsgall=[]
gswatbofile=None

#贝叶斯优化：初始化
class MHGPSWAT_INIT(tornado.web.RequestHandler):
    def post(self):
        global gcount
        global gopt
        global gindex
        global gTotalNumber
        global gmsgreturn
        global gIter
        global gmsgall
        #记录推荐时间
        global gswatbofile
        
        gswatbofile=open('./fail-suggest.txt','w')
        
        gmsgall=[]
        gIter=0
        #自动率定中，第一个Job启动ncores个Task,JobID:-1,ncores个Tasks返回时，每次启动一个新的Job,ID自0递增
        gmsgreturn=[]
        gcount=0
        
        #Tornado随机启动56组参数，Spring接收，启动56个Task
        print(self.request.remote_ip)
        #接收Json数据结构
        body2=tornado.escape.json_decode(self.request.body)
        ncores=56
        gTotalNumber=ncores
        print(body2)
        #参数名称
        lname=[]
        #参数范围
        lrange=[]
        #参数ID索引
        list=[]
        #-1标识
        list.append([gcount])
        lpid2=[]
        for ele in body2:
            lname.append(ele['name'])
            lrange.append([ele['min'],ele['max']])
            lpid2.append(ele['pid'])
        gindex=lpid2
        list.append(lpid2)
        gproblem = {
        'num_vars': len(lname),
        'names': lname,
        'groups': None,
        'bounds': lrange
    }
        #初始化Optimizer
        print('lrange')
        print(lrange)
        print(gproblem)
        #优化器初始化
        #.....1:GP过程，采集函数选择：acq_func=“LCB”，“EI”，“PI”，“gp_hedge”
        gopt=Optimizer(lrange, "GP")
        print("gopt")
        #.....2:Random Search
        #gopt=Optimizer(dimensions=lrange,base_estimator="dummy",acq_optimizer="sampling")
        
        #得到问题参数空间
        print(gproblem)
        #采用Latin采样方法
        import SALib.sample.latin
        param_values = SALib.sample.latin.sample(gproblem, 1000)
        print("Latin sampling finished")
        #参数列表赋值
        #gX=param_values
        #得到总体采样个数，即发给集群任务总数，供result中计数用。发多少要收多少
        #gTotalNumber=len(param_values)
        #发回给请求端
        #随机从Latin采样中选择58组
        import random
        for index in range(ncores):
            ele=param_values[random.randint(0,len(param_values))]
            #print(ele)
            #生成字典
            #dic=dict(zip(lpid,ele))
            #arrary 转list
            list.append(ele.tolist())
            #list.append(A(ele[0],ele[1],ele[2]).__dict__)
        #得到ncores组参数
        print(len(list))
        objstr=json.dumps(list)
        print(objstr)
        self.write(objstr)
        
        
    def get(self):
        print(self.request.remote_ip)   
        
#贝叶斯优化：返回单个优化结果
class MHGPSWAT_SINGLE(tornado.web.RequestHandler):
    def post(self):
        global gcount
        global gopt
        global gindex
        global gTotalNumber
        global gmsgreturn
        global gmsgall
        global gIter
        global gswatbofile
        
        #JobID,自0递增。-1标识第一个Job,内含ncores个Task
        #print(self)
        #从1开始
        gcount=gcount+1
        #接收Task返回的结果 [index,24parameters,nes1,nes2,nes3...avgnes] 
        body2=tornado.escape.json_decode(self.request.body)
        #SA中body2[0]标识SAMPLE INDEX，采样编号。在BO中[0]标识ncores个Task标识
        print(body2)
        next_x=body2[1][:len(body2[1])-4]
        next_y=body2[1][len(body2[1])-1]
        next_y=1-next_y
        print('Here show parameters & results from MR TASKS,nse is')
        #print(next_x)
        print(body2[1][len(body2[1])-1])
        timebefore=datetime.now()
        #更新概率函数
        gopt.tell(tuple(next_x),next_y)
        suggest_x=gopt.ask()
        timeafter=datetime.now()
        timecost=timeafter-timebefore
        print("sugget cost time is ..................")
        print((timecost*1000).seconds)
        gswatbofile.writelines(str((timecost*1000).seconds))
        gswatbofile.writelines("\n")        
        gmsgreturn.append(suggest_x)
        
        #收集完整轮ncores个
        if(gcount==gTotalNumber):
            gIter=gIter+1     
            print("第"+str(gIter)+"轮")
            if(gIter==2):
                res=gopt.get_result()
                print(res)
                dump(res,'fail.pkl')
                gswatbofile.close()
                return

            gmsgall=[]
            gmsgall.append([gIter])
            gmsgall.append(gindex)
            gmsgall=gmsgall+gmsgreturn

            print(gmsgall)
            print('Here show suggested ')
            import requests#导入request模块
            import json#导入json模块
            #url="http://172.16.224.129:8080/bocontinue"
            #url="http://localhost:8080/calibrate/bocontinue"
            url="http://localhost:8080/bocontinue"
            data_json = json.dumps(gmsgall)#转化成json类型
            print("启动新JobID")
            try:
                response=requests.post(url=url,data=data_json,timeout=1)
        #print(response.status_code)
                print(response.text)
            except Exception as e:
                print('sending to Spring to create Job')
            gmsgreturn=[]
            gcount=0
        #发生请求
    def get(self):
        print(self.request.remote_ip)   
        

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(CustomEncoder, self).default(obj)

def main():
    app=tornado.web.Application(
            [
                (r'/BOPARAM0',MHGPSWAT_INIT),
                (r'/BORESULT0',MHGPSWAT_SINGLE),
                ],
            )

    app.listen(9999)
    tornado.ioloop.IOLoop.instance().start()

if __name__=='__main__':
    main()