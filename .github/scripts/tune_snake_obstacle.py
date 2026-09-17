from pathlib import Path
import py_compile


def replace_exact(path: str, old: str, new: str, expected: int = 1) -> None:
    file_path = Path(path)
    text = file_path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != expected:
        raise RuntimeError(f"{path}: expected {expected} occurrences, found {count}: {old!r}")
    file_path.write_text(text.replace(old, new), encoding="utf-8")


replace_exact(
    "sac/config.py",
    "    obstacle_clear_reward: float = 8.0\n    stall_weight: float = 0.18\n",
    "    obstacle_clear_reward: float = 8.0\n    front_lift_weight: float = 3.0\n    stall_weight: float = 0.18\n",
)
replace_exact(
    "sac/config.py",
    "    joint_action_scale: Tuple[float, ...] = (1.10, 1.10, 1.10, 1.10)\n",
    "    joint_action_scale: Tuple[float, ...] = (1.40, 0.35, 1.40, 0.35)\n",
)
replace_exact("sac/config.py", "    track_speed_center: float = 4.0\n", "    track_speed_center: float = 3.0\n")
replace_exact(
    "sac/config.py",
    "    obstacle_clear_margin: float = 0.10\n    initial_ground_clearance: float = 0.003\n",
    "    obstacle_clear_margin: float = 0.10\n    front_lift_approach_distance: float = 0.45\n    front_lift_target_margin: float = 0.02\n    front_stage_height_margin: float = 0.015\n    initial_ground_clearance: float = 0.003\n",
)
replace_exact(
    "sac/config.py",
    "    warmup_action_limit: float = 0.50\n    obstacle_height_curriculum:",
    "    warmup_action_limit: float = 1.00\n    warmup_hold_steps: int = 25\n    obstacle_height_curriculum:",
)

replace_exact(
    "sac/env.py",
    "    def _physics_is_finite(self) -> bool:\n        arrays = (self.data.qpos, self.data.qvel, self.data.qacc, self.data.ctrl, self.track_omega, self.track_angle)\n        return bool(all(np.isfinite(array).all() for array in arrays))\n\n    def _align_support_with_ground(self) -> None:\n",
    "    def _physics_is_finite(self) -> bool:\n        arrays = (self.data.qpos, self.data.qvel, self.data.qacc, self.data.ctrl, self.track_omega, self.track_angle)\n        return bool(all(np.isfinite(array).all() for array in arrays))\n\n    def _geom_bottom_z(self, geom_id: int) -> float:\n        geom_id = int(geom_id)\n        rotation = self.data.geom_xmat[geom_id].reshape(3, 3)\n        half_extent_z = float(np.dot(np.abs(rotation[2, :]), self.model.geom_size[geom_id]))\n        return float(self.data.geom_xpos[geom_id, 2] - half_extent_z)\n\n    def _front_tip_state(self) -> Tuple[float, float]:\n        front_tip_geom_id = int(self.front_track_pad_ids[0])\n        progress = self._course_progress(self.data.geom_xpos[front_tip_geom_id, :2])\n        return float(progress), self._geom_bottom_z(front_tip_geom_id)\n\n    def _align_support_with_ground(self) -> None:\n",
)
replace_exact(
    "sac/env.py",
    "        self.stage_front_track = False\n        self.stage_base = False\n        self.stage_back_track = False\n        self.obstacle_cleared = False\n",
    "        self.stage_front_track = False\n        self.stage_base = False\n        self.stage_back_track = False\n        self.obstacle_cleared = False\n        self.previous_front_lift_quality = 0.0\n",
    expected=2,
)

old_stage = '''    def _update_stage_flags(self) -> Dict[str, float]:
        rewards = {"front_stage": 0.0, "base_stage": 0.0, "rear_stage": 0.0, "clear_stage": 0.0}
        front_progress = self._course_progress(self.data.xpos[self.front_track_body_id, :2])
        base_progress = self._course_progress(self.data.xpos[self.base_id, :2])
        rear_progress = self._course_progress(self.data.xpos[self.back_track_body_id, :2])
        if not self.stage_front_track and front_progress >= self.obstacle_top_start_progress:
            self.stage_front_track = True
            rewards["front_stage"] = self.reward_cfg.front_track_stage_reward
        if not self.stage_base and base_progress >= self.obstacle_top_start_progress:
            self.stage_base = True
            rewards["base_stage"] = self.reward_cfg.base_stage_reward
        if not self.stage_back_track and rear_progress >= self.obstacle_top_start_progress:
            self.stage_back_track = True
            rewards["rear_stage"] = self.reward_cfg.rear_track_stage_reward
        if not self.obstacle_cleared and rear_progress >= self.obstacle_end_progress + self.cfg.obstacle_clear_margin:
            self.obstacle_cleared = True
            rewards["clear_stage"] = self.reward_cfg.obstacle_clear_reward
        return rewards
'''
new_stage = '''    def _update_stage_flags(self) -> Dict[str, float]:
        rewards = {"front_stage": 0.0, "base_stage": 0.0, "rear_stage": 0.0, "clear_stage": 0.0}
        front_tip_progress, front_tip_z = self._front_tip_state()
        base_progress = self._course_progress(self.data.xpos[self.base_id, :2])
        rear_progress = self._course_progress(self.data.xpos[self.back_track_body_id, :2])
        front_stage_min_z = self.obstacle_height - self.cfg.front_stage_height_margin
        if not self.stage_front_track and front_tip_progress >= self.obstacle_top_start_progress and front_tip_z >= front_stage_min_z:
            self.stage_front_track = True
            rewards["front_stage"] = self.reward_cfg.front_track_stage_reward
        if not self.stage_base and base_progress >= self.obstacle_top_start_progress:
            self.stage_base = True
            rewards["base_stage"] = self.reward_cfg.base_stage_reward
        if not self.stage_back_track and rear_progress >= self.obstacle_top_start_progress:
            self.stage_back_track = True
            rewards["rear_stage"] = self.reward_cfg.rear_track_stage_reward
        if not self.obstacle_cleared and rear_progress >= self.obstacle_end_progress + self.cfg.obstacle_clear_margin:
            self.obstacle_cleared = True
            rewards["clear_stage"] = self.reward_cfg.obstacle_clear_reward
        return rewards
'''
replace_exact("sac/env.py", old_stage, new_stage)

replace_exact(
    "sac/env.py",
    "        track_torque_penalty = float(mean_track_torque_sq / max(self.cfg.track_torque_limit ** 2, 1e-6))\n        reward = cfg.progress_weight * progress_delta + cfg.heading_weight * heading_reward + cfg.forward_speed_weight * forward_speed + stage_rewards[\"front_stage\"] + stage_rewards[\"base_stage\"] + stage_rewards[\"rear_stage\"] + stage_rewards[\"clear_stage\"] - cfg.stall_weight * stall_penalty - cfg.reverse_weight * reverse_penalty - cfg.lateral_drift_weight * lateral_penalty - cfg.action_rate_weight * action_rate_penalty - cfg.action_acceleration_weight * action_acceleration_penalty - cfg.joint_pose_weight * joint_pose_penalty - cfg.joint_velocity_weight * joint_velocity_penalty - cfg.joint_torque_weight * joint_torque_penalty - cfg.track_torque_weight * track_torque_penalty - cfg.time_penalty\n        terms = {\"total\": float(reward), \"progress\": progress_delta, \"heading\": float(heading_reward), \"forward_speed\": forward_speed,",
    "        track_torque_penalty = float(mean_track_torque_sq / max(self.cfg.track_torque_limit ** 2, 1e-6))\n        front_tip_progress, front_tip_z = self._front_tip_state()\n        distance_to_obstacle = self.obstacle_start_progress - front_tip_progress\n        lift_window = not self.stage_front_track and -0.03 <= distance_to_obstacle <= self.cfg.front_lift_approach_distance\n        lift_target_z = self.obstacle_height + self.cfg.front_lift_target_margin\n        if lift_window:\n            lift_denominator = max(lift_target_z - self.cfg.initial_ground_clearance, 1e-6)\n            front_lift_quality = float(np.clip((front_tip_z - self.cfg.initial_ground_clearance) / lift_denominator, 0.0, 1.0))\n            front_lift_delta = front_lift_quality - self.previous_front_lift_quality\n            self.previous_front_lift_quality = front_lift_quality\n        else:\n            front_lift_quality = 0.0\n            front_lift_delta = 0.0\n            self.previous_front_lift_quality = 0.0\n        front_lift_reward = cfg.front_lift_weight * front_lift_delta\n        reward = cfg.progress_weight * progress_delta + cfg.heading_weight * heading_reward + cfg.forward_speed_weight * forward_speed + front_lift_reward + stage_rewards[\"front_stage\"] + stage_rewards[\"base_stage\"] + stage_rewards[\"rear_stage\"] + stage_rewards[\"clear_stage\"] - cfg.stall_weight * stall_penalty - cfg.reverse_weight * reverse_penalty - cfg.lateral_drift_weight * lateral_penalty - cfg.action_rate_weight * action_rate_penalty - cfg.action_acceleration_weight * action_acceleration_penalty - cfg.joint_pose_weight * joint_pose_penalty - cfg.joint_velocity_weight * joint_velocity_penalty - cfg.joint_torque_weight * joint_torque_penalty - cfg.track_torque_weight * track_torque_penalty - cfg.time_penalty\n        terms = {\"total\": float(reward), \"progress\": progress_delta, \"heading\": float(heading_reward), \"forward_speed\": forward_speed, \"front_lift_reward\": float(front_lift_reward), \"front_lift_quality\": float(front_lift_quality), \"front_tip_z\": float(front_tip_z), \"distance_to_obstacle\": float(distance_to_obstacle),",
)

replace_exact(
    "sac/train.py",
    "    last_metrics = None\n    last_step = start_step\n\n    try:\n",
    "    last_metrics = None\n    last_step = start_step\n    warmup_action = np.zeros(cfg.action_dim, dtype=np.float32)\n\n    try:\n",
)
replace_exact(
    "sac/train.py",
    "            if start_step == 0 and collected_steps <= cfg.start_steps:\n                limit = TRAIN_CONFIG.warmup_action_limit\n                action = np.random.uniform(-limit, limit, cfg.action_dim).astype(np.float32)\n            else:\n                action = agent.select_action(obs, deterministic=False)\n",
    "            if start_step == 0 and collected_steps <= cfg.start_steps:\n                limit = TRAIN_CONFIG.warmup_action_limit\n                if collected_steps == 1 or (collected_steps - 1) % TRAIN_CONFIG.warmup_hold_steps == 0:\n                    warmup_action = np.random.uniform(-limit, limit, cfg.action_dim).astype(np.float32)\n                action = warmup_action.copy()\n            else:\n                action = agent.select_action(obs, deterministic=False)\n",
)

for file_name in ("sac/config.py", "sac/env.py", "sac/train.py"):
    py_compile.compile(file_name, doraise=True)

Path(".github/workflows/tune-obstacle-exploration.yml").unlink(missing_ok=True)
Path(".github/scripts/tune_snake_obstacle.py").unlink(missing_ok=True)
