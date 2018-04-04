#!/bin/bash

../build/tools/caffe train \
	--solver="solver.prototxt" \
	--snapshot="models/Car_Logo_512x512_iter_97000.solverstate" 

