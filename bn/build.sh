mkdir build
cd build

cmake -DCMAKE_PREFIX_PATH=/usr/include/c++/11/libtorch ..
cmake --build . --config Release

cmake -DCMAKE_PREFIX_PATH=`python3 -c 'import torch;print(torch.utils.cmake_prefix_path)'` ..

./bn