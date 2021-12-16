
import java.io.IOException;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;


public class WordCount {

	public static void main(String[] args) throws IOException, ClassNotFoundException, InterruptedException {
		Configuration conf = new Configuration();
		
//		conf.set("mapreduce.input.fileinputformat.split.maxsize", "" + 64*1024*1024);
//		conf.set("mapreduce.input.fileinputformat.split.minsize", "" + 256*1024*1024);
		conf.set("mapreduce.framework.name","local");
	    conf.set("fs.defaultFS","file:///");
	    conf.set("mainkey","mainvalue");
	    
		String inputpath="input.txt";
		String outputpath="d://output";
		Path outputfolder = new Path(outputpath);
		
		Job job = Job.getInstance(conf);
		conf.set("newmainkey","helloworldmainvalue");
		//设置jar
		job.setJarByClass(WordCount.class);
		job.setNumReduceTasks(1);
		//设置Mapper相关的属性
		job.setMapperClass(WCMapper.class);
		job.setMapOutputKeyClass(Text.class);
		job.setMapOutputValueClass(LongWritable.class);
		FileInputFormat.setInputPaths(job, new Path(inputpath));//words.txt
		
		//设置Reducer相关属性
		job.setReducerClass(WCReducer.class);
		job.setOutputKeyClass(Text.class);
		job.setOutputValueClass(LongWritable.class);
		
        if (outputfolder.getFileSystem(conf).exists(outputfolder)) {
            outputfolder.getFileSystem(conf).delete(outputfolder, true);
        }
		
		FileOutputFormat.setOutputPath(job, new Path(outputpath));
		
		//job.setCombinerClass(WCReducer.class);
				
		//提交任务
		job.waitForCompletion(true);
	}

}
