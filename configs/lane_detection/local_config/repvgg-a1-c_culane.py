# Data pipeline
from configs.lane_detection.common.datasets.culane_seg import dataset
from configs.lane_detection.common.datasets.train_level0_288 import train_augmentation
from configs.lane_detection.common.datasets.test_288 import test_augmentation

# Optimization pipeline
#from configs.lane_detection.common.optims.segloss_center_7class import loss
from configs.lane_detection.common.optims.sgd02 import optimizer
from configs.lane_detection.common.optims.ep50_poly_warmup200 import lr_scheduler


loss = dict(
    name='CenterLaneLoss',
    existence_weight=0.1,
    center_weight=0.1,
    ignore_index=255,
    weight=[0.4, 1, 1, 1, 1]
)

# Default args that can be overridden in commandline
train_args_default = dict(
    exp_name='repvgg-a1-c_baseline_culane',
    workers=5,
    batch_size=10,
    checkpoint=None,
    # Device args
    world_size=2,
    dist_url='tcp://localhost:12345',
    device='cuda',
    val_num_steps=0,  # Seg IoU validation (mostly useless)
    save_dir='./checkpoints'
)
test_args_default = dict(
    exp_name='repvgg-a1-c_baseline_culane',
    workers=10,
    batch_size=80,
    checkpoint='./checkpoints/repvgg-a1-c_culane/model.pt',
    # Device args
    device='cuda',
    save_dir='./checkpoints'
)

# Configs
train = dict(
    input_size=(288, 800),
    original_size=(590, 1640),
    num_classes=5,
    num_epochs=12,
    collate_fn=None,  # 'dict_collate_fn' for LSTR
    seg=True  # Seg-based method or not
)
train.update(train_args_default)

test = dict(
    seg=True,
    gap=20,
    ppl=18,
    thresh=0.3,
    collate_fn=None,  # 'dict_collate_fn' for LSTR
    input_size=(288, 800),
    original_size=(590, 1640),
    max_lane=4,
    dataset_name='culane'
)
test.update(test_args_default)

model = dict(
    name='DLabV1AuxLane',
    backbone_cfg=dict(
        name='RepVggEncoder',
        backbone_name='RepVGG-A1',
        pretrained=True,
        deploy=False,
        fpn=False
    ),
    reducer_cfg=dict(
        name='RESAReducer',
        in_channels=1280,
        reduce=128
    ),
    lane_classifier_cfg=dict(
        name='SimpleLaneExist',
        num_output=5 - 1,
        flattened_size=4500,
    ),
    classifier_cfg=dict(
        name='DeepLabV1Head',
        in_channels=128,
        num_classes=5,
        dilation=1
    )
)
