# Copyright (c) 2024-2026 Ziqi Fan
# SPDX-License-Identifier: Apache-2.0

"""Keep main's APX tasks usable alongside the migrated legacy/V1.1 replays."""

from pathlib import Path

import pytest


@pytest.mark.parametrize("terrain,iterations", [("Flat", 20000), ("Rough", 50000)])
def test_apx_training_config_resolves_with_isaac_lab_3(terrain, iterations):
    from isaaclab_tasks.utils import resolve_task_config

    import robot_lab.tasks  # noqa: F401

    task = f"RobotLab-Isaac-Velocity-{terrain}-Opendoge-Apx-v0"
    env, runner = resolve_task_config(task, "rsl_rl_cfg_entry_point", overrides=[])
    assert runner.max_iterations == iterations
    assert runner.actor.hidden_dims == [512, 256, 128]
    assert runner.critic.hidden_dims == [512, 256, 128]
    assert runner.actor.obs_normalization is False
    assert runner.experiment_name == f"opendoge_apx_{terrain.lower()}"
    assert (
        Path(env.scene.robot.spawn.asset_path).as_posix().endswith("opendoge/apx_description/urdf/apx_description.urdf")
    )
    assert env.scene.robot.actuators["base_legs"].actuator_effort_limit == 28
    assert env.scene.robot.actuators["base_legs"].actuator_velocity_limit == 28
    assert env.events.randomize_rigid_body_mass_base.params["mass_distribution_params"] == (-0.5, 0.5)
    if terrain == "Flat":
        assert env.scene.height_scanner is None
        assert env.scene.terrain.terrain_type == "plane"
