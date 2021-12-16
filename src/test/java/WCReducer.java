
import java.io.IOException;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

public class WCReducer extends Reducer<Text, LongWritable, Text, LongWritable> {

	
	@Override
	protected void setup(Reducer<Text, LongWritable, Text, LongWritable>.Context context)
			throws IOException, InterruptedException {
		// TODO Auto-generated method stub
		Configuration conf=context.getConfiguration();
		System.out.println("reduce setup is calling.......................");
		System.out.println("map value is: "+conf.get("mapkey"));
		System.out.println("all configuration value is from HDFS, only readable: "+conf.get("mainkey"));
		System.out.println(context.getJobName());
		System.out.println(context.getNumReduceTasks());
		System.out.println(context.getJobID());
		System.out.println(context.getCurrentKey());
		System.out.println(context.getCurrentValue());
	}

	@Override
	protected void reduce(Text key, Iterable<LongWritable> v2s, Context context)
			throws IOException, InterruptedException {
		System.out.println("reduce is calling");
		System.out.println("Key is "+key);
		//定义一行计数器
		long sum = 0;
		//迭代他的次数
		for(LongWritable lw : v2s){
			//求和
			sum += lw.get();
		}
		//输出
		context.write(key, new LongWritable(sum));
	}

	
}
