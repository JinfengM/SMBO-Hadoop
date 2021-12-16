

import java.io.IOException;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.lib.input.FileSplit;

public class WCMapper extends Mapper<LongWritable, Text, Text, LongWritable> {

	@Override
	protected void setup(Mapper<LongWritable, Text, Text, LongWritable>.Context context)
			throws IOException, InterruptedException {
		// TODO Auto-generated method stub
		Configuration conf=context.getConfiguration();
		conf.set("mapkey", "mapvalue");
		conf.set("mainkey", "newmainvalue2");
		System.out.println(conf.get("mapred.tasktracker.reduce.tasks.maximum"));
		/*
		System.out.println("map setup is calling............................");
		System.out.println(conf.get("mapreduce.framework.name"));
		System.out.println(conf.get("mainkey"));
		System.out.println(conf.get("newmainkey"));
		*/
		/* 这里能够向context里面写东西？ */
		String k1=((FileSplit)context.getInputSplit()).getPath().getParent().toUri().getPath();
		String k2=((FileSplit)context.getInputSplit()).getPath().getName();
		k1=k1+","+k2;
		context.write(new Text(k1), new LongWritable(1));
	}

	@Override
	protected void map(LongWritable key, Text value, Context context)
			throws IOException, InterruptedException {
		//接收一行数据
		//System.out.println("mapper:"+context.getConfiguration().get("mapkey")+"  "+context.getConfiguration().get("mainkey"));
		String line = value.toString();
		System.out.println(line);
		//分割
		String[] words = line.split(" ");
		//迭代
		for(String w : words){
			//发送
			//context.write(new Text(w), new LongWritable(1));
		}
	}

	
}
