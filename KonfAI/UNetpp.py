from konfai.network import network
import segmentation_models_pytorch as smp
import torch

class Head(network.ModuleArgsDict):

    def __init__(self):
        super().__init__()
        self.add_module("Tanh", torch.nn.Tanh())

class UNetpp(network.Network):
    
    def __init__(self,
                optimizer : network.OptimizerLoader = network.OptimizerLoader(),
                schedulers: dict[str, network.LRSchedulersLoader] = {
                    "default:ReduceLROnPlateau": network.LRSchedulersLoader(0)
                },
                outputs_criterions: dict[str, network.TargetCriterionsLoader] = {"default" : network.TargetCriterionsLoader()},
                nb_channel : int = 5):
        super().__init__(in_channels = nb_channel, optimizer = optimizer, schedulers = schedulers, outputs_criterions = outputs_criterions, dim = 2)
        self.add_module("model", smp.UnetPlusPlus(
            encoder_name="resnet34",
            encoder_weights=None, 
            in_channels=nb_channel,
            classes=1,  
            activation=None  
        ))
        self.add_module("Head", Head())

if __name__ == "__main__":
    model = UNetpp()
    total = sum(p.numel() for p in model.parameters())
    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)

    print(f"Total parameters: {total}")
    print(f"Trainable parameters: {trainable}")