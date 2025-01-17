![ALT](/media/images/System.png "Deep RL System Overview")

# CuLE 0.1.0

_CuLE 0.1.0 - July 2019_

CuLE is a CUDA port of the Atari Learning Environment (ALE) and is
designed to accelerate the development and evaluation of deep
reinforcement algorithms using Atari games. Our CUDA Learning
Environment (CuLE) overcomes many limitations of existing CPU- based
Atari emulators and scales naturally to multi-GPU systems.  It leverages
the parallelization capability of GPUs to run thousands of Atari games
simultaneously; by rendering frames directly on the GPU, CuLE avoids the
bottleneck arising from the limited CPU-GPU communication bandwidth.

# Compatibility

CuLE performs best when compiled with the [CUDA 10.0 Toolkit](https://developer.nvidia.com/cuda-toolkit).
It is currently incompatible with CUDA 10.1.

We have tested the following environments.

|**Operating System** | **Compiler** |
|-----------------|----------|
| Ubuntu 16.04 | GCC 5.4.0 |
| Ubuntu 18.04 | GCC 7.3.0 |

CuLE runs successfully on the following NVIDIA GPUs, and it is expected to be efficient on
any Maxwell-, Pascal-, Volta-, and Turing-architecture NVIDIA GPUs.

|**GPU**|
|---|
|NVIDIA Tesla P100|
|NVIDIA Tesla V100|
|NVIDIA TitanV|

# Building CuLE

```
$ git clone --recursive https://github.com/DanielShrimpton/cule
$ python setup.py install
```

# Project Structure

```
cule/
  cule/
  env/
  examples/
  media/
  third_party/
  torchcule/
```

Several example programs are also distributed with the CuLE library. They are
contained in the following directories.

```
examples/
  a2c/
  dqn/
  ppo/
  vtrace/
  utils/
  visualize/
```

# Docker 

The reccomended (and easiest) way of using CuLE is through Docker.
We assume nvidia-docker is already installed in your system.
To build the CuLE image you can use the following docker file - create a file named "Dockerfile" in your preferred folder and copy the following text into it:

```
FROM nvidia/cuda:10.0-cudnn7-devel-ubuntu18.04 as base
RUN apt-get update
RUN apt-get install -y python3.6
RUN apt-get install -y python3-pip
RUN ln -s /usr/bin/python3.6 /usr/bin/python
RUN ln -s /usr/bin/pip3 /usr/bin/pip
RUN apt-get -y install git

RUN pip install torch==1.2.0
RUN pip install torchvision==0.4.0

RUN pip install psutil
RUN pip install pytz
RUN pip install tqdm
RUN pip install atari_py

RUN git clone https://github.com/NVIDIA/apex
RUN pip install --upgrade pip
RUN cd apex && pip install -v --global-option="--cpp_ext" --global-option="--cuda_ext" ./

RUN apt-get install -y libsm6 libxrender-dev
RUN pip install opencv-python

RUN pip install cython
RUN apt-get install zlib1g-dev
RUN git clone --recursive https://github.com/NVLabs/cule
RUN cd cule && python setup.py install
```

Once the docker file has been created and saved, you can build the docker image by typing (in the same folder of the docker file):

```
sudo nvidia-docker build -t cule_release .
```

You can then run the following command to access a CuLE-ready terminal:

```
sudo nvidia-docker run -it -t cule_release bash
```

You have now access to CuLE and can run different algorithms, including DQN, PPO, A2C, and A2C+V-trace.
A2C+V-trace uses the best batching strategy to leverage the high troughput generated by CuLE.
To replicate the same results reported in our paper (e.g. reaching an average score of 18 for Pong in less than 3 minutes using a single GPU) you can run the following commands:

```
cd cule\examples\vtrace
python vtrace_main.py --env-name PongNoFrameskip-v4 --normalize --use-cuda-env --num-ales 1200 --num-steps 20 --num-steps-per-update 1 --num-minibatches 20 --t-max 8000000 --evaluation-interval 200000
```

The parameters passed to vtrace_main.py specify: the name of the environment (--env-name PongNoFrameskip-v4, same naming convention adopted in OpenAIGym, all our environments are -v4); normalization of the input images (--normalize, this is the normalization procedure normaly adopted in RL for Atari games; notice that, with no normalization, convergence takes way more time); the use of GPU to simulate the environments (--use-cuda-env; if you want to use OpenAI instead, use --use-openai; if you want to use the CuLE CPU backend to generate data, do not specify any of these two); the total number of environments simulated (--num-ales 1200; for an effective use of CuLE, use a large number of environments); the number of steps in the buffer used to compute the discounted rewards (--num-steps 20; if the number of steps is too large, you may saturate the memory); the number of steps after which a DNN update is computed (--num-steps-per-update 1, meaning that an update is computed after each CuLE steps trhough all the environments); the number of minibatches in the total population of environments (in this case --num-minibatches 20 guarantees that each minibatch, composed by 1200 / 20 = 60 environments, advances by 20 steps before using its data to update the DNN; since there are exactly 20 minibatches and one update is computed at each step, it means that for any step simulated by CuLE one batch is providing training data the the GPU for the update; each experience is used only once for training in this case - with other configurations the same experience may be used multiple times, for a more sample efficient data generation strategy; where data between different batches are however correlated); the total number of steps to be performed in training (--t-max 8000000); and the total number of steps to evaluate the DNN on the testing environments (--evaluation-interval 200000). 
The CuLE CPU backend is used by default for testing. If you want to use OpenAIGym instead, use --use-openai-test-env. 

# Citing

```
@inproceedings{NEURIPS2020_e4d78a6b,
 author = {Dalton, Steven and frosio, iuri},
 booktitle = {Advances in Neural Information Processing Systems},
 editor = {H. Larochelle and M. Ranzato and R. Hadsell and M. F. Balcan and H. Lin},
 pages = {19773--19782},
 publisher = {Curran Associates, Inc.},
 title = {Accelerating Reinforcement Learning through GPU Atari Emulation},
 url = {https://proceedings.neurips.cc/paper/2020/file/e4d78a6b4d93e1d79241f7b282fa3413-Paper.pdf},
 volume = {33},
 year = {2020}
}

@misc{dalton2019gpuaccelerated,
   title={GPU-Accelerated Atari Emulation for Reinforcement Learning},
   author={Steven Dalton and Iuri Frosio and Michael Garland},
   year={2019},
   eprint={1907.08467},
   archivePrefix={arXiv},
   primaryClass={cs.LG}
}
```

# About

CuLE is released by NVIDIA Corporation as Open Source software under the
3-clause "New" BSD license.

# Copyright

Copyright (c) 2017-2019, NVIDIA CORPORATION.  All rights reserved.

```
  Redistribution and use in source and binary forms, with or without modification, are permitted
  provided that the following conditions are met:
      * Redistributions of source code must retain the above copyright notice, this list of
        conditions and the following disclaimer.
      * Redistributions in binary form must reproduce the above copyright notice, this list of
        conditions and the following disclaimer in the documentation and/or other materials
        provided with the distribution.
      * Neither the name of the NVIDIA CORPORATION nor the names of its contributors may be used
        to endorse or promote products derived from this software without specific prior written
        permission.

  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR
  IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
  FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL NVIDIA CORPORATION BE LIABLE
  FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
  BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
  OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
  STRICT LIABILITY, OR TOR (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```
