# Copyright (C) 2020 Istituto Italiano di Tecnologia (IIT). All rights reserved.
# This software may be modified and distributed under the terms of the
# GNU Lesser General Public License v2.1 or any later version.

if(FRAMEWORK_COMPILE_Estimators)
  set(H_PREFIX include/BipedalLocomotion/Estimators)
  add_bipedal_locomotion_library(
    NAME                   Estimators
    SOURCES                src/RecursiveLeastSquare.cpp
    PUBLIC_HEADERS         ${H_PREFIX}/RecursiveLeastSquare.h
    SUBDIRECTORIES         tests/Estimators
    PUBLIC_LINK_LIBRARIES  BipedalLocomotion::ParametersHandler BipedalLocomotion::System Eigen3::Eigen)
endif()

if(FRAMEWORK_COMPILE_FloatingBaseEstimators)
  set(H_PREFIX include/BipedalLocomotion/FloatingBaseEstimators)
  add_bipedal_locomotion_library(
    NAME                   FloatingBaseEstimators
    SOURCES                src/ModelComputationsHelper.cpp src/FloatingBaseEstimator.cpp src/InvariantEKFBaseEstimator.cpp src/LeggedOdometry.cpp
    SUBDIRECTORIES         tests/FloatingBaseEstimators
    PUBLIC_HEADERS         ${H_PREFIX}/FloatingBaseEstimatorParams.h ${H_PREFIX}/FloatingBaseEstimatorIO.h ${H_PREFIX}/FloatingBaseEstimator.h ${H_PREFIX}/InvariantEKFBaseEstimator.h ${H_PREFIX}/LeggedOdometry.h ${H_PREFIX}/ModelComputationsHelper.h
    PUBLIC_LINK_LIBRARIES  BipedalLocomotion::ParametersHandler BipedalLocomotion::ManifConversions iDynTree::idyntree-high-level iDynTree::idyntree-core iDynTree::idyntree-model BipedalLocomotion::System Eigen3::Eigen BipedalLocomotion::Contacts iDynTree::idyntree-modelio-urdf
    PRIVATE_LINK_LIBRARIES MANIF::manif)
endif()
