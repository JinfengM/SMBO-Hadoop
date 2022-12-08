# SMBO-Hadoop
	SMBO-Hadoop is an improved Hadoop-based cloud for complex model simulation optimization. It can parallelize conventional sequential-model-based optimization (SMBO) methods and guarantees the reliability of simulation optimization tasks by handling node failures as well.

Purposes

SMBO-Hadoop is an improved Hadoop-based cloud for complex model simulation optimization. It can parallelize conventional sequential-model-based optimization (SMBO) methods and guarantees the reliability of simulation optimization tasks by handling node failures as well.

The framework clarifies how cloud techniques can be practically applied to efficiently alleviate the substantial computational burden of complex model simulation optimization, with lessons for future studies to reduce model simulation time and handle partial failure.

Installation
1. Hadoop High Availability (HA) cluster is required,version 2.7.5 is preferable. Details can be referred to https://hadoop.apache.org/docs/r2.7.5/hadoop-project-dist/hadoop-hdfs/HDFSHighAvailabilityWithNFS.html#Deployment
2. Anaconda is recommended to host Tornado web server. Tornado is used to accommodate sequential-model-based optimization, for example Bayesian optimization algorithm. Python libraries including numpy, skopt, pandas, keras are also required. Details can be referred to souce code of "BayesianOptimizationServer.py"
3. SpringBoot is responsible for receiving the candidate points (suggested parameter sets) from Tornado, and then writing a driver program to run these model evaluations on the Hadoop cluster.

Functionality and workflow

The improved Hadoop-based cloud framework is dedicated to complex model simulation optimization. It consists of two improvements: Improvement 1: The traditional sequential-model-based algorithm, such as Bayesian optimizaiton (BO), can be parallelized in the framework by grouping multiple simulations into multiple sequential MapReduce jobs. Multiple tasks inside a job are invoked and executed in parallel. Improvement 2: The efficiency of a single simulation is further improved by invoking a single model computation in a Mapper container only, without using the Reducer procedure.Below is the schematic digram of the framework

![20210413第二篇文章框架制图CLIP](https://user-images.githubusercontent.com/96234482/146670614-ce996cb5-1846-4542-a7bf-206d70fc1ba7.png)
Schematic diagram of the improved Hadoop-based cloud framework dedicated to complex model simulation optimization (Quoted from https://doi.org/10.1016/j.envsoft.2022.105330)

Cite

Title = "Improved Hadoop-based cloud for complex model simulation optimization: Calibration of SWAT as an example"

Doi = "https://doi.org/10.1016/j.envsoft.2022.105330"

Url = "https://www.sciencedirect.com/science/article/pii/S1364815222000366"
