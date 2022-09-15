# -*- coding: utf-8 -*-
"""
Created on Fri Feb 11 01:41:22 2022

@author: user
"""
#%%
from Data_Synthesis import ThomsonParabolaSpec, OutputPlane, validatedeflection, Beam, Run, Image
import numpy as np
import time
import matplotlib.pyplot as pl

#%% Parameters for system setup
mass_MeV = 938.28
charge_e = 1
thermal_E_MeV = 5
E_max_MeV = 5
E_min_MeV = 0

Collimator_mm = 120
Collimator_diameter_micron = 200


E_strength_kV = 2
B_strength_mT = 100
#B_strength_mT = r'circular_magnet.mat'
Thomson_Plane_mm = 170
dimensions_mm = [10, 50, 50]

Detector_Plane_mm = 320
Detector_dimensions_mm = [100, 100]

Thomson = ThomsonParabolaSpec(E_strength_kV, B_strength_mT, Thomson_Plane_mm, dimensions_mm)
Detector = OutputPlane(Detector_Plane_mm, Detector_dimensions_mm)
 

#%% Propagate Proton  
Propagation_step_size =  10 ** -10

Proton_beam = Beam(Collimator_mm, Collimator_diameter_micron, mass_MeV, charge_e).generate_beam(4000, thermal_E_MeV, E_max_MeV)

x_list, y_list, E_list, x_init_list, y_init_list = Run(Proton_beam, Thomson, Detector, Propagation_step_size)

pl.plot(x_list, y_list, "x", label = "Proton detection")  
pl.legend()
pl.xlabel("Deflection in x / m")
pl.ylabel("Deflection in y / m")
pl.show()  

 #%% Generate Image

x_range_mm = [0, 25]
y_range_mm = [0, 25]
pixels = [28, 28]

weight = 0.6
background_noise = 10
abberations = 0.2
hard_hit_noise_fraction = 0.1
detector_threshold = 255
zero_point_micron = 200

h = Image.generate_image(x_list, y_list, E_list, pixels, x_range_mm, y_range_mm)
#%%
y = Image.add_noise(h, weight, background_noise, abberations, hard_hit_noise_fraction, detector_threshold, zero_point_micron, x_range_mm, y_range_mm)
pl.imshow(y.T, cmap='hot', origin='lower')
pl.colorbar()

#%% Investigate Suitable step size
step_sizes = np.logspace(-13, -9, 20)
error_list = []
computation_time = []
for step_size in step_sizes:
    print(f"Running step size {step_size}")
    start = time.time()
    x_diff, y_diff = validatedeflection(mass_MeV, charge_e, 0.1, 10, 0.1, Thomson, Detector, "Euler", num_step = step_size)
    end = time.time()
    computation_time.append(end - start)
    error_list.append(x_diff + y_diff)

pl.plot(error_list, computation_time, "x", color="tab:blue", label="Data")       
pl.plot(error_list, computation_time, "--", color="tab:blue")     
pl.ylabel("Computation time (s)")
pl.xlabel("Total percentage error (%)")
pl.xscale("log")
pl.yscale("log")
pl.legend()
