# -*- coding: utf-8 -*-
"""
Created on February 2026

@author: RafaelSalgueiro58 & cheritie
"""

# imports
from OOPAO.tools.interpolateGeometricalTransformation import interpolate_image
import matplotlib.pyplot as plt

class Shift:
    def __init__(self, shift_x:list,
                 shift_y:list,
                 shift_angle:list):

        """
        A Shift object consists ...

        Parameters
        ----------
        """

        self.shift_x = shift_x
        self.shift_y = shift_y
        self.shift_angle = shift_angle
        self.tag = 'EM_shift'

    def relay(self, src):

        self.src = src
        if src.tag == 'source':
            self.src_list = [src]
        elif src.tag == 'asterism':
            self.src_list = src.src

        for i,src in enumerate(self.src_list):

            src.optical_path.append([self.tag, self])

            # src.fluxMap[i*40:(i+1)*40,:] = 0
            # src.OPD_no_pupil += self.OPD

            # shift the EM field amplitude
            src.fluxMap = interpolate_image(image_in = src.fluxMap,
                                            pixel_size_in = 1.0,
                                            pixel_size_out = 1.0,
                                            resolution_out = len(src.fluxMap),
                                            rotation_angle = self.shift_angle[i],
                                            shift_x = self.shift_x[i],
                                            shift_y = self.shift_y[i],
                                            anamorphosisAngle = 0,
                                            tangentialScaling = 0,
                                            radialScaling = 0,
                                            shape_out = None,
                                            order = 1)

            plt.figure()
            plt.imshow(src.fluxMap)
            plt.colorbar()
            plt.show()

            # plt.figure()
            # plt.imshow(src.OPD_no_pupil)
            # plt.colorbar()
            # plt.show()

            # shift the EM OPD and phase
            src.OPD = interpolate_image(image_in = src.OPD.copy(),
                                                 pixel_size_in = 1.0,
                                                 pixel_size_out = 1.0,
                                                 resolution_out = len(src.OPD.copy()),
                                                 rotation_angle = self.shift_angle[i],
                                                 shift_x = self.shift_x[i],
                                                 shift_y = self.shift_y[i],
                                                 anamorphosisAngle = 0,
                                                 tangentialScaling = 0,
                                                 radialScaling = 0,
                                                 shape_out = None,
                                                 order = 1)

            print("test")

            plt.figure()
            plt.imshow(src.OPD)
            plt.colorbar()
            plt.show()

            plt.figure()
            plt.imshow(src.OPD_no_pupil)
            plt.colorbar()
            plt.show()

            plt.figure()
            plt.imshow(src.phase)
            plt.colorbar()
            plt.show()