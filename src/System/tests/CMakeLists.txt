# Copyright (C) 2020 Istituto Italiano di Tecnologia (IIT). All rights reserved.
# This software may be modified and distributed under the terms of the
# GNU Lesser General Public License v2.1 or any later version.

add_bipedal_test(
  NAME VariablesHandler
  SOURCES VariablesHandlerTest.cpp
  LINKS BipedalLocomotion::System)

add_bipedal_test(
  NAME IntegratorTest
  SOURCES IntegratorTest.cpp
  LINKS BipedalLocomotion::System Eigen3::Eigen)
