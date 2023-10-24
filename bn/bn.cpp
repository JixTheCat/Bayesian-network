 #include <torch/torch.h>
 #include <iostream>

// class Z
// {
//       double& mean;
//       double& std;
//   public:
//     Z(double& mean, double& std) : mean(mean), std(std) { }
//     operator torch::normal() { return torch::normal(mean, std, 1); }
// };
// torch::Tensor dist = torch::normal(0.0, 1.0, 3);

int main() {

  // double mean;
  // double std;
  torch::Tensor dist = torch::normal(0.0, 1.0, 3);
  std::cout << "basic operation" << std::endl;
  std::cout << dist << std::endl;
  
  std::cout << "roll the dice..." << std::endl;
  double mean = 0;
  double std = 1;
  auto dice = [&](){ return torch::normal(mean, std, 1); };
  std::cout << dice() << std::endl;

  std::cout << "roll the dice again..." << std::endl;
  mean = 5;
  std = 1;
  std::cout << dice() << std::endl;

  std::cout << "roll dice of dice..." << std::endl;
  auto new_dice = [&](){ return torch::normal(dice().item<double>(), std, 1); };
  std::cout << new_dice() << std::endl;

  std::cout << "roll the dicedice again..." << std::endl;
  mean = 0;
  std = 1;
  std::cout << dice() << std::endl;

  // Z z(mean, std)

  // mean = 0;
  // std = 1;

  // std::cout << "roll the dice..." << std::endl;
  // std::cout << z << std::endl;

  // std::cout << "roll new dice..." << std::endl;
  // mean = 5;
  // std = 1;
  // std::cout << z << std::endl;
}

// struct Node {
//   char name;
//   torch::normal(, 1) distribution;
// }
