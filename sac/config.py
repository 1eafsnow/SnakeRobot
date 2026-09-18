from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Tuple


PROJECT_DIR = Path(__file__).resolve().parent.parent / "description"
JOINT_NAMES = ("front_joint1", "front_joint2", "back_joint1", "back_joint2")
ACTUATOR_NAMES = ("f1_motor", "f2_motor", "b1_motor", "b2_motor")
FRONT_TRACK_PAD_NAMES = ("front_track_pad1_geom", "front_track_pad2_geom", "front_track_pad3_geom")
BACK_TRACK_PAD_NAMES = ("back_track_pad1_geom", "back_track_pad2_geom", "back_track_pad3_geom")
SUPPORT_GEOM_NAMES = FRONT_TRACK_PAD_NAMES + BACK_TRACK_PAD_NAMES + ("base_link_pad",)


@dataclass(frozen=True)
class RewardConfig:
    progress_weight: float = 16.0
    heading_weight: float = 0.10
    forward_speed_weight: float = 0.18
    front_track_stage_reward: float = 2.0
    base_stage_reward: float = 5.0
    rear_track_stage_reward: float = 7.0
    obstacle_clear_reward: float = 10.0
    front_lift_weight: float = 3.0
    rear_lift_weight: float = 4.0
    arch_clearance_weight: float = 3.0
    body_obstacle_contact_weight: float = 0.35
    body_obstacle_force_weight: float = 1.25
    body_obstacle_force_scale: float = 40.0
    stall_weight: float = 0.18
    reverse_weight: float = 1.5
    lateral_drift_weight: float = 0.10
    action_rate_weight: float = 0.03
    action_acceleration_weight: float = 0.01
    joint_pose_weight: float = 0.005
    joint_velocity_weight: float = 0.005
    joint_torque_weight: float = 0.005
    track_torque_weight: float = 0.005
    time_penalty: float = 0.003
    success_reward: float = 25.0
    termination_penalty: float = 12.0
    invalid_physics_penalty: float = 30.0


@dataclass(frozen=True)
class EnvConfig:
    xml_path: Path = PROJECT_DIR / "mjcf" / "scene_slider.xml"
    base_name: str = "base_link"
    front_track_body_name: str = "front_track"
    back_track_body_name: str = "back_track"
    free_joint_name: str = "floating_base"
    floor_name: str = "floor"
    lidar_site_name: str = "lidar_site"
    obstacle_geom_name: str = "training_obstacle"
    obstacle_hfield_name: str = "training_obstacle_hfield"
    base_pad_name: str = "base_link_pad"
    joint_names: Tuple[str, ...] = JOINT_NAMES
    actuator_names: Tuple[str, ...] = ACTUATOR_NAMES
    front_track_pad_names: Tuple[str, ...] = FRONT_TRACK_PAD_NAMES
    back_track_pad_names: Tuple[str, ...] = BACK_TRACK_PAD_NAMES
    support_geom_names: Tuple[str, ...] = SUPPORT_GEOM_NAMES
    q_nominal: Tuple[float, ...] = (0.0, 0.0, 0.0, 0.0)
    kp: Tuple[float, ...] = (20.0, 20.0, 20.0, 20.0)
    kd: Tuple[float, ...] = (5.0, 5.0, 5.0, 5.0)
    joint_action_scale: Tuple[float, ...] = (1.40, 0.35, 1.40, 0.35)
    joint_limit_margin: float = 0.10
    frame_skip: int = 20
    max_episode_steps: int = 750
    action_filter_alpha: float = 0.15
    action_rate_limit: float = 8.0
    track_effective_radius: float = 0.075
    track_virtual_inertia: float = 0.08
    track_motor_damping: float = 0.20
    track_kd: float = 8.0
    track_torque_limit: float = 36.0
    track_speed_center: float = 3.0
    track_speed_scale: float = 6.0
    track_speed_limit: float = 15.0
    lidar_rows: int = 4
    lidar_cols: int = 120
    lidar_hfov_deg: float = 120.0
    lidar_vfov_deg: float = 45.0
    lidar_max_range: float = 30.0
    lidar_scan_hz: float = 10.0
    lidar_group: int = 0
    floor_lidar_group: int = 5
    hfield_rows: int = 5
    hfield_cols: int = 501
    hfield_center_x: float = -2.5
    hfield_center_y: float = 0.0
    hfield_base_z: float = -10.0
    hfield_radius_x: float = 2.5
    hfield_radius_y: float = 2.5
    obstacle_max_supported_height: float = 0.18
    hfield_base_depth: float = 0.10
    obstacle_min_height: float = 0.10
    obstacle_height_limit: float = 0.17
    obstacle_distance_range: Tuple[float, float] = (1.05, 1.35)
    obstacle_ramp_length_range: Tuple[float, float] = (0.05, 0.08)
    obstacle_platform_length_range: Tuple[float, float] = (0.16, 0.24)
    goal_after_obstacle_range: Tuple[float, float] = (1.00, 1.35)
    goal_lateral_range: Tuple[float, float] = (-0.08, 0.08)
    goal_radius: float = 0.30
    obstacle_clear_margin: float = 0.10
    front_lift_approach_distance: float = 0.45
    front_lift_target_margin: float = 0.02
    front_stage_height_margin: float = 0.015
    rear_lift_approach_distance: float = 0.60
    rear_lift_target_margin: float = 0.02
    base_stage_height_margin: float = 0.015
    rear_stage_height_margin: float = 0.015
    arch_clearance_margin: float = 0.010
    privileged_obstacle_distance_scale: float = 1.0
    initial_ground_clearance: float = 0.003
    initial_yaw_noise_deg: float = 3.0
    joint_position_noise: float = 0.02
    joint_velocity_noise: float = 0.03
    base_position_xy_noise: float = 0.02
    base_linear_velocity_noise: float = 0.02
    base_angular_velocity_noise: float = 0.03
    max_tilt_deg: float = 75.0
    min_base_height: float = 0.04
    max_base_height: float = 1.20
    world_xy_limit: float = 4.80
    max_lateral_deviation: float = 0.90
    goal_position_scale: float = 4.5
    linear_velocity_scale: float = 1.0
    angular_velocity_scale: float = 3.0
    joint_velocity_scale: float = 8.0
    reward: RewardConfig = field(default_factory=RewardConfig)


@dataclass(frozen=True)
class SACConfig:
    obs_dim: int = 520
    action_dim: int = 6
    hidden_dims: Tuple[int, ...] = (512, 512)
    gamma: float = 0.995
    tau: float = 0.005
    actor_lr: float = 3e-4
    critic_lr: float = 3e-4
    alpha_lr: float = 2e-4
    batch_size: int = 512
    replay_size: int = 400_000
    start_steps: int = 10_000
    update_after: int = 10_000
    updates_per_step: int = 1
    initial_alpha: float = 0.10
    target_entropy: Optional[float] = -3.0
    log_std_min: float = -5.0
    log_std_max: float = 0.5
    reward_scale: float = 0.20
    gradient_clip: float = 10.0
    total_steps: int = 2_000_000
    device: str = "auto"


@dataclass(frozen=True)
class TrainConfig:
    seed: int = 42
    total_steps: int = 2_000_000
    checkpoint_every: int = 100_000
    eval_every: int = 50_000
    eval_episodes: int = 8
    log_updates_every: int = 5_000
    warmup_action_limit: float = 1.00
    warmup_hold_steps: int = 25
    obstacle_height_curriculum: Tuple[Tuple[int, float], ...] = (
        (0, 0.110),
        (250_000, 0.125),
        (600_000, 0.140),
        (1_000_000, 0.155),
        (1_500_000, 0.170),
    )


ENV_CONFIG = EnvConfig()
SAC_CONFIG = SACConfig()
TRAIN_CONFIG = TrainConfig()
