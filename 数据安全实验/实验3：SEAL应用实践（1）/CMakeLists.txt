cmake_minimum_required(VERSION 3.10) 
project(Experiment2)
add_executable(ckks_example ckks_example.cpp)
add_compile_options(-std=c++17)

find_package(SEAL)
target_link_libraries(ckks_example SEAL::seal)
