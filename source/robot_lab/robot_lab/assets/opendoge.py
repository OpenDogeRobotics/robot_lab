# Copyright (c) 2024-2026 Ziqi Fan
# SPDX-License-Identifier: Apache-2.0

"""Original OpenDoge articulation, ported from OpenDoge_train (see SOURCE_LICENSE).

This asset intentionally uses the original joint axes and stance, not OpenDog V1.1.
"""

from isaaclab_newton.sim.schemas import NewtonArticulationCfg
from isaaclab_physx.sim.schemas import PhysxArticulationCfg, PhysxRigidBodyCfg

import isaaclab.sim as sim_utils
from isaaclab.actuators import DCMotorCfg, IdealPDActuatorCfg
from isaaclab.assets import ArticulationCfg

from robot_lab.assets import ROBOT_LAB_ASSETS_DIR

OPENDOGE_CFG = ArticulationCfg(
    prim_path="/World/Robot",
    spawn=sim_utils.UrdfFileCfg(
        asset_path=str(ROBOT_LAB_ASSETS_DIR / "Robots/opendoge/urdf/Opendoge.urdf"),
        fix_base=False,
        merge_fixed_joints=False,
        activate_contact_sensors=True,
        rigid_props=PhysxRigidBodyCfg(
            linear_damping=0.0,
            angular_damping=0.0,
            max_linear_velocity=20.0,
            max_angular_velocity=9.5,
            max_depenetration_velocity=1.0,
        ),
        articulation_props=[
            PhysxArticulationCfg(
                enabled_self_collisions=False, solver_position_iteration_count=4, solver_velocity_iteration_count=1
            ),
            NewtonArticulationCfg(self_collision_enabled=False),
        ],
        joint_drive=sim_utils.UrdfConverterCfg.JointDriveCfg(
            gains=sim_utils.UrdfConverterCfg.JointDriveCfg.PDGainsCfg(stiffness=0.0, damping=0.0)
        ),
    ),
    init_state=ArticulationCfg.InitialStateCfg(
        pos=(0.0, 0.0, 0.15),
        joint_pos={".*_hip_joint": 0.0, ".*_thigh_joint": 0.6, ".*_calf_joint": -1.5},
        joint_vel={".*": 0.0},
    ),
    soft_joint_pos_limit_factor=0.9,
    actuators={
        "legs": IdealPDActuatorCfg(
            joint_names_expr=[".*_joint"],
            stiffness=12.0,
            damping=0.5,
            armature=0.005,
            friction=0.0,
            joint_effort_limit=1.0e9,
            actuator_effort_limit={".*_hip_joint": 6.0, ".*_thigh_joint": 6.0, ".*_calf_joint": 9.0},
            actuator_velocity_limit={".*_hip_joint": 10.472, ".*_thigh_joint": 10.472, ".*_calf_joint": 6.981},
        )
    },
)

# APX configuration retained from main (2024-2025 jayjayhust, Apache-2.0).
# APX is a separate robot; its URDF/meshes must be supplied by the user.
OPENDOGE_APX_CFG = OPENDOGE_CFG.copy()
OPENDOGE_APX_CFG.spawn.asset_path = str(
    ROBOT_LAB_ASSETS_DIR / "Robots/opendoge/apx_description/urdf/apx_description.urdf"
)
OPENDOGE_APX_CFG.spawn.merge_fixed_joints = True
OPENDOGE_APX_CFG.spawn.replace_cylinders_with_capsules = False
OPENDOGE_APX_CFG.spawn.rigid_props.max_linear_velocity = 1000.0
OPENDOGE_APX_CFG.spawn.rigid_props.max_angular_velocity = 1000.0
OPENDOGE_APX_CFG.spawn.articulation_props[0].solver_velocity_iteration_count = 0
OPENDOGE_APX_CFG.init_state.pos = (0.0, 0.0, 0.4)
OPENDOGE_APX_CFG.init_state.joint_pos = {".*_hip_joint": 0.0, ".*_thigh_joint": 0.8, ".*_calf_joint": -1.5}
OPENDOGE_APX_CFG.actuators = {
    "base_legs": DCMotorCfg(
        joint_names_expr=[".*_hip_joint", ".*_thigh_joint", ".*_calf_joint"],
        joint_effort_limit=1.0e9,
        actuator_effort_limit=28,
        saturation_effort=28,
        actuator_velocity_limit=28,
        stiffness=20.0,
        damping=0.7,
        friction=0.0,
    ),
}
