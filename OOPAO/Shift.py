# -*- coding: utf-8 -*-
"""
Created on February 2026

@author: RafaelSalgueiro58 & cheritie
"""

# imports
from OOPAO.tools.interpolateGeometricalTransformation import interpolate_image
from OOPAO.tools.tools import OopaoError

class Shift:
    def __init__(self, shift_x:list,
                 shift_y:list,
                 rot_angle:list):

        """
        Shift object allows to shit the Electromagnetic field (EMF), i.e., both phase and amplitude
        It can be applied both for single sources or asterisms with several sources
        This object allows simulating Super Resolution, namely with SH wavefront sensors, by shifting each EMF before
        propagating towards the SH wfs

        Parameters
        ----------

        shift_x : list
        List containing the shits in the direction x for each guide star considered in units of pixels
        Sub-pixel shifts are possible (0.5, 0.25 or other)

        shift_y : list
        List containing the shits in the direction y for each guide star considered in units of pixels
        Sub-pixel shifts are possible (0.5, 0.25 or other)

        rot_angle : list
        List containing the angular rotations for each guide star considered in units of degrees

        ************************** EXEMPLE **************************

        shift = Shift(shift_x,shift_y,rot_angle)

        ast**atm*tel*shift

        --> EM field is propagated from ast --> atm --> tel, and then the EM field from each guide star of the asterism
        is properly shifted and/rotated according to the given shift_x, shift_y and rot_angle given as input.

        """

        self.shift_x = shift_x
        self.shift_y = shift_y
        self.rot_angle = rot_angle
        self.tag = 'EM_shift'

    def relay(self, src):

        self.src = src
        if src.tag == 'source':
            self.src_list = [src]
        elif src.tag == 'asterism':
            self.src_list = src.src

        # verify if the given shift and rotation lists have the proper length, i.e. the number of guide stars
        lists = [self.shift_x, self.shift_y, self.rot_angle]
        lengths = {len(lst) for lst in lists}
        if lengths != {len(self.src_list)}:
            raise OopaoError('The given shift and rotation lists need to have a length equal to the number of sources')

        for i,src in enumerate(self.src_list):

            src.optical_path.append([self.tag, self])

            # shift the EM field amplitude (fluxMap)
            src.fluxMap = interpolate_image(image_in = src.fluxMap.copy(),
                                            pixel_size_in = 1.0,
                                            pixel_size_out = 1.0,
                                            resolution_out = len(src.fluxMap.copy()),
                                            rotation_angle = self.rot_angle[i],
                                            shift_x = self.shift_x[i],
                                            shift_y = self.shift_y[i],
                                            anamorphosisAngle = 0,
                                            tangentialScaling = 0,
                                            radialScaling = 0,
                                            shape_out = None,
                                            order = 1)

            # shift the EM OPD and phase
            # by updating the OPD, the phase (and OPD_no_pupil) will be also updated accordingly automatically
            src.OPD = interpolate_image(image_in = src.OPD.copy(),
                                        pixel_size_in = 1.0,
                                        pixel_size_out = 1.0,
                                        resolution_out = len(src.OPD.copy()),
                                        rotation_angle = self.rot_angle[i],
                                        shift_x = self.shift_x[i],
                                        shift_y = self.shift_y[i],
                                        anamorphosisAngle = 0,
                                        tangentialScaling = 0,
                                        radialScaling = 0,
                                        shape_out = None,
                                        order = 1)