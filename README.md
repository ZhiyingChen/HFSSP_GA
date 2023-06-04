# HFSSP_GA

**Problem**

This is a project to solve Hybrid Flow Shop Scheduling Problem (HFSSP) using genetic algorithm.

In HFSSP, each job (workpiece) has to be processed through $M$ stages in sequence. There are $N$ jobs and each job passes through each stage in turn.
In each stage $m$, there are $m_k$ machines available. The duration of each job processed at each stage is a prerequisite.

The constraints are as follows.

    1) All machines in the same stage are identical;
    
    2) In a given stage, each job can be processed on any machine;
    
    3) At any given moment, each job can be processed on at most one machine;
    
    4) At any given moment, each machine can process at most one job;
    
    5) The process of each job is not allowed to be interrupted at any stage.

The objective is to get a sequence of all jobs so that the total makespan is minimized.


**Environment Deployment**

 Install Python Executor (version >= 3.7.0), Anaconda IDE is recommanded


The required packages are listed in requirements.txt. you can install them using:

    pip install -r requirements.txt
 
 **Run**

To run project:

    1. put your parameters in main.py
    2. execute python main.py

 **Result**

The result will be given in a csv file called *output.csv* after the project (main.py) is successfully executed. Then, you can execute python gantt.py to get a gantt plot of *output.csv*.

An example is given as follows. 

![排产结果示例图](https://github.com/ZhiyingChen/HFSSP_GA/blob/master/images/gantt_example.png)

This is a result of six jobs finished by three operations with the duration matrix as follows.

$$
matrix = [
    [2, 4, 6],
    [4, 9, 2],
    [4, 2, 8],
    [9, 5, 6],
    [5, 2, 7],
    [9, 4, 3]
]
$$

There are two machines available for each operation.

  

