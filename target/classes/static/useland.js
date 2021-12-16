/**
 * Created with JetBrains WebStorm.
 * User: LIANGHZ
 * Date: 18-11-15
 * Time: 上午11:08
 * To change this template use File | Settings | File Templates.
 */
/**
 * Created with JetBrains WebStorm.
 * User: LIANGHZ
 * Date: 18-6-22
 * Time: 上午10:17
 * To change this template use File | Settings | File Templates.
 */
//基础数据
//var ip = "localhost:8080/calibrate";
var ip = "localhost:8080";
var info = null;
$(document).ready(function() {
	
});//61222833
Date.prototype.Format = function (fmt) { //author: meizz
    var o = {
        "M+": this.getMonth() + 1, //月份
        "d+": this.getDate(), //日
        "h+": this.getHours(), //小时
        "m+": this.getMinutes(), //分
        "s+": this.getSeconds(), //秒
        "q+": Math.floor((this.getMonth() + 3) / 3), //季度
        "S": this.getMilliseconds() //毫秒
    };
    if (/(y+)/.test(fmt)) fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
    for (var k in o)
        if (new RegExp("(" + k + ")").test(fmt)) fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
    return fmt;
}


function lusetest() {
    var url = "http://"+ip+"/luse_const";
    var str = '[1,2,3,4,5,1,2,3,4,5,1,2,3,4,5,1,2,3]';
    var config = {
	    async:false,
	    xhrFields: {
	        withCredentials: true
	    },
	    url: url,
	    type: "POST",
	    data:str,
        dataType: 'json',
	    beforeSend: function () {
	    	ctrldisable();
	    },
	    success: function(result) {
	        //alert(result);
	        ctrlenable();
	        var txt = JSON.stringify(result, null, 2);
	        document.getElementById('jsontext').value = txt;
	    },
	    error: function(r){
	        alert('已发送，返回错误');
	        ctrlenable()
	    },
	    failed: function(r){
	        alert('failed');
	        ctrlenable()
	    }
	};
	$.ajax(config);
};

function sendpythoncreate() {
    var url = "http://"+ip+"/luse_const";
    var str = 'createlusetopython';
    var config = {
	    async:false,
	    xhrFields: {
	        withCredentials: true
	    },
	    url: url,
	    type: "POST",
	    data:str,
        dataType: 'json',
	    beforeSend: function () {
	    	ctrldisable();
	    },
	    success: function(result) {
	        //alert(result);
	        ctrlenable();
	        var txt = JSON.stringify(result, null, 2);
	        document.getElementById('jsontext').value = txt;
	    },
	    error: function(r){
	        alert('已发送，返回错误');
	        ctrlenable()
	    },
	    failed: function(r){
	        alert('failed');
	        ctrlenable()
	    }
	};
	$.ajax(config);
};

function ctrlenable()
{
	var b = false;
	document.getElementById('lusetest').disable = b;
}
function ctrldisable()
{
	var b = true;
	document.getElementById('lusetest').disable = b;
}
