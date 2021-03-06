import pytest
pytestmark = pytest.mark.floating_base_estimators

import bipedal_locomotion_framework.bindings as blf
import numpy as np

def test_legged_odometry():
    # This function just performs an interface test for
    # the generated python bindings,

    # create KinDynComputationsDescriptor
    kindyn_handler = blf.StdParametersHandler()
    kindyn_handler.set_parameter_string("model_file_name", "./model.urdf")
    kindyn_handler.set_parameter_vector_string("joints_list", ["neck_pitch", "neck_roll", "neck_yaw",
                                                               "torso_pitch", "torso_roll", "torso_yaw",
                                                               "l_shoulder_pitch", "l_shoulder_roll", "l_shoulder_yaw",
                                                               "l_elbow",
                                                               "r_shoulder_pitch", "r_shoulder_roll", "r_shoulder_yaw",
                                                               "r_elbow",
                                                               "l_hip_pitch", "l_hip_roll", "l_hip_yaw",
                                                               "l_knee", "l_ankle_pitch", "l_ankle_roll",
                                                               "r_hip_pitch", "r_hip_roll", "r_hip_yaw",
                                                               "r_knee", "r_ankle_pitch", "r_ankle_roll"])
    kindyn_desc = blf.construct_kindyncomputations_descriptor(kindyn_handler)
    assert kindyn_desc.is_valid()

    dt = 0.01
    # create configuration parameters handler for legged odometry
    lo_params_handler = blf.StdParametersHandler()
    lo_params_handler.set_parameter_float("sampling_period_in_s", dt)

    model_info_group = blf.StdParametersHandler()
    model_info_group.set_parameter_string("base_link", "root_link")
    # use same frame for the IMU - requirement due to the software design
    model_info_group.set_parameter_string("base_link_imu", "root_link")
    # unused parameters but required for configuration (will be deprecated soon)
    model_info_group.set_parameter_string("left_foot_contact_frame", "l_foot")
    model_info_group.set_parameter_string("right_foot_contact_frame", "r_foot")
    assert(lo_params_handler.set_group("ModelInfo", model_info_group))

    lo_group = blf.StdParametersHandler()
    lo_group.set_parameter_string("initial_fixed_frame", "l_sole")
    lo_group.set_parameter_string("initial_ref_frame_for_world", "l_sole")
    lo_group.set_parameter_vector_float("initial_world_orientation_in_ref_frame",  [1.0, 0.0, 0.0, 0.0])
    lo_group.set_parameter_vector_float("initial_world_position_in_ref_frame",  [0.0, 0.0, 0.0])
    lo_group.set_parameter_string("switching_pattern",  "useExternal")
    assert lo_params_handler.set_group("LeggedOdom", lo_group)

    # instantiate legged odometry
    legged_odom = blf.LeggedOdometry()
    empty_handler = blf.StdParametersHandler()
    # assert passing an empty parameter handler to false
    assert legged_odom.initialize(empty_handler, kindyn_desc.kindyn) == False

    # assert passing an properly configured parameter handler to true
    assert legged_odom.initialize(lo_params_handler, kindyn_desc.kindyn) == True

    # shape of the robot for the above specified joints list
    encoders = np.array([-0.0001, 0.0000, 0.0000,
                          0.1570, 0.0003, -0.0000,
                         -0.0609, 0.4350, 0.1833,
                          0.5375,
                         -0.0609, 0.4349, 0.1834,
                          0.5375,
                          0.0895, 0.0090, -0.0027,
                         -0.5694, -0.3771, -0.0211,
                          0.0896, 0.0090, -0.0027,
                         -0.5695, -0.3771, -0.0211])
    encoder_speeds = np.zeros_like(encoders)

    for time in np.arange(start=0, step=dt, stop=10*dt):
        fixed_frame_idx = legged_odom.get_fixed_frame_index()

        # here we only fill measurement buffers
        assert(legged_odom.set_kinematics(encoders, encoder_speeds))
        contact_name = "l_sole"
        contact_status = True
        switch_time = time
        time_now = time
        assert legged_odom.set_contact_status(contact_name, contact_status, switch_time, time_now)

        # since we set "switching_pattern" parameter to "useExternal"
        # we can change the fixed frame manually from an external script
        # such as this script, where for example, we change the same
        # frame as we had earlier initialized the estimator
        # if the "switching_pattern" is not set to `useExternal`
        # this function call will return false
        legged_odom.change_fixed_frame(fixed_frame_idx)

        # computations given the set measurements
        assert legged_odom.advance()

        # sample asserts for show-casing outputs
        out = legged_odom.get()
        assert len(out.base_twist) == 6
        assert len(out.state.imu_linear_velocity) == 3
