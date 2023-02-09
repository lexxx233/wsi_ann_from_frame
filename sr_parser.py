import numpy as np
import math
from shapely.geometry import Polygon
from dcm_utils import *
from configs import *

class Ann_Handler:

    @staticmethod
    def rectangify_polygon(coordinates):
        """
        Convert an arbitary polygonal shapes into a rectangle which cover the entire the polygon
        by identifying the outer bound of the polygon annotation

        :param coordinates: array of vertices on polygon
        :return: Polygon rectangle
        """

        xmin, ymin = 999999, 999999  # This is the top left corner of the rectangle
        xmax, ymax = 0, 0  # This is the bottom right corner of the rectangle

        for point in coordinates:
            xmin = xmin if point[0] > xmin else point[0]
            ymin = ymin if point[1] > ymin else point[1]
            xmax = xmax if point[0] < xmax else point[0]
            ymax = ymax if point[1] < ymax else point[1]

        p0 = (xmin, ymin)
        p1 = (xmin, ymax)
        p2 = (xmax, ymax)
        p3 = (xmax, ymin)

        return [p0, p1, p2, p3]

    @staticmethod
    def divide_frame(area_coordiate, x_dim, y_dim):
        """
        Divide a rectangular polygon into sub rectangular polygon of size x_dim by y_dim

        :param area_coordiate:
        :param x_dim:
        :param y_dim:
        :return:
        """
        sub_frames = []

        rect_width = area_coordiate[2][0] - area_coordiate[0][0]
        rect_height = area_coordiate[2][1] - area_coordiate[0][1]

        assert (rect_width > 0 and rect_height > 0)

        num_x_frames = int(math.ceil(rect_width / x_dim))
        num_y_frames = int(math.ceil(rect_height / y_dim))

        for ix in range(num_x_frames):
            for iy in range(num_y_frames):
                sub_p0 = (area_coordiate[0][0] + ix * x_dim, area_coordiate[0][1] + iy * y_dim)
                sub_p1 = (area_coordiate[0][0] + ix * x_dim, area_coordiate[0][1] + (iy + 1) * y_dim)
                sub_p2 = (area_coordiate[0][0] + (ix + 1) * x_dim, area_coordiate[0][1] + (iy + 1) * y_dim)
                sub_p3 = (area_coordiate[0][0] + (ix + 1) * x_dim, area_coordiate[0][1] + iy * y_dim)

                sub_frames.append([sub_p0, sub_p1, sub_p2, sub_p3])

        return sub_frames

    @staticmethod
    def is_rect_ann_in_frame(polygon_coordinates, frame_coordinates):
        """
        Check whether a rectangular frame is within a polygonal shaped annotation

        :param polygon_coordinates:
        :param frame_coordinates:
        :return: Boolean value whether the frame is within the annotated region
        """

        ann = Polygon(polygon_coordinates)
        frame = Polygon(frame_coordinates)

        return frame.intersects(ann) and frame.intersection(ann).area > 0

    @staticmethod
    def get_frame_coordinates_within_ann(polygon_coordinates, x_frame_dim, y_frame_dim):
        """
        Return all frames of desired size within a polygonal annotation.

        :param polygon_coordinates:
        :param x_frame_dim:
        :param y_frame_dim:
        :return:
        """

        # Rectangify the polygon mask
        rect_ann = Ann_Handler.rectangify_polygon(polygon_coordinates)
        # Divide rectangle mask into sub frames of desired size
        all_frames = Ann_Handler.divide_frame(rect_ann, x_frame_dim, y_frame_dim)

        collected_frames = []
        for frame in all_frames:
            # Check if each sub frame is within the polygon annotation areas, if it is, put it in collected_frames
            if Ann_Handler.is_rect_ann_in_frame(polygon_coordinates, frame):
                collected_frames.append(frame)

        return collected_frames

    @staticmethod
    def get_polygon_from_sr(sr_dcm):
        """
        Recursively reading through SR document to find polygon annotations
        :param input_dcm:
        :param sr_dcm:
        :return:
        """

        relationship_type =get_meta_data(sr_dcm, *RELATIONSHIP_TYPE)
        value_type =get_meta_data(sr_dcm, *VALUE_TYPE)
        seqs =get_meta_data(sr_dcm, *CONTENT_SEQUENCE)

        polygon = []

        if not seqs:  # Termination condition
            if relationship_type.value == 'CONTAINS' and value_type.value == 'SCOORD3D':
                graphic_type = get_meta_data(sr_dcm, *GRAPHIC_TYPE)
                graphic_data = get_meta_data(sr_dcm, *GRAPHIC_DATA)
                if graphic_type.value == 'POLYGON':
                    return graphic_data.value
                else:
                    return
            else:
                return

        for seq in seqs:
            temp = Ann_Handler.get_polygon_from_sr(seq)
            if temp == None:
                continue

            if len(temp) > 0:
                polygon.append(temp)

        return polygon

    @staticmethod
    def convert_sr_polygon_to_polygon(sr_polygons):
        """
        Convert 3d SR polygon nested lists to list of 2d polygon tuples
        :param sr_polygons:
        :return:
        """
        polygons = []

        for sr_poly in sr_polygons[0]:
            vertices = sr_poly[0]
            polygon = []
            for i in range(int(len(vertices) / 3)):
                polygon.append((vertices[3 * i], vertices[3 * i + 1]))
            polygons.append(polygon)

        return polygons




