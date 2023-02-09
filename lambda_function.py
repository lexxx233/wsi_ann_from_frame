import json
from sr_parser import *
import boto3
from wsidicom import WsiDicom
import os
import pydicom
from pathlib import Path


def make_img_wsi(slide, collected_frame, level=1):
    region = slide.read_region_mm((collected_frame[0]), level, (
        collected_frame[2][0] - collected_frame[0][0], collected_frame[2][1] - collected_frame[0][1]))

    return region


def lambda_handler(event, context):
    os.mkdir('/tmp/dcm')
    os.mkdir('/tmp/annotation')
    os.mkdir('/tmp/img')

    # Parse lambda event from a REST API and get parameters named 'dicom_path' and 'annotation_path' and 'sampleid
    event_body = json.loads(event['body'])
    dicom_path = event_body["dicom_path"]
    annotation_path = event_body["annotation_path"]
    sampleid = event_body["sampleid"]

    # Loop through the dicom_path and annotation_path to get all the files from s3 bucket 'bright-field-dev',
    # download it to /tmp folder and get the path to the downloaded files to be used in the next step
    s3 = boto3.client('s3')

    for i in range(len(dicom_path)):
        with open('/tmp/dcm/' + dicom_path[i] + '.dcm', 'wb') as data:
            s3.download_fileobj('pacs-dicom-dev', dicom_path[i], data)
            # open the downloaded dicom file and check if there is any pixel data
            # if there is no pixel data, then delete the file and download the next file
            try:
                ds = pydicom.dcmread('/tmp/dcm/' + dicom_path[i] + '.dcm')
                ds.pixel_array.any()
            except:
                print('No pixel data or not a valid dcm in ' + dicom_path[i] + '.dcm')
                os.remove('/tmp/dcm/' + dicom_path[i] + '.dcm')
                continue

        print(dicom_path[i] + '.dcm' + ' downloaded successfully')

    for i in range(len(annotation_path)):
        with open('/tmp/annotation/' + dicom_path[i] + '.dcm', 'wb') as data:
            s3.download_fileobj('pacs-dicom-dev', annotation_path[i], data)

    wsi_dicom = WsiDicom.open('/tmp/dcm/')

    for annotation in Path('/tmp/annotation/').glob('*.dcm'):
        sr_dataset = pydicom.dcmread(annotation)
        sr_polygons = Ann_Handler.get_polygon_from_sr(sr_dataset)
        polygons = Ann_Handler.convert_sr_polygon_to_polygon(sr_polygons)

        for polygon in polygons:
            collected_frames = Ann_Handler.get_frame_coordinates_within_ann(polygon, X_PX_SPACING * FRAME_WIDTH,
                                                                            Y_PX_SPACING * FRAME_HEIGHT)

            for frame in collected_frames:
                img = make_img_wsi(wsi_dicom, frame, 1)
                img.save('/tmp/img/' + str(frame[0][0]) + '_' + str(frame[0][1]) + '.jpg')

    # Upload images to s3 bucket 'bright-field-dev' with path 'sampleid/'
    for i in Path('/tmp/img/').glob('*.jpg'):
        s3.upload_file('/tmp/img/' + i.name, 'bright-field-dev', sampleid + '/' + i.name)

    # Create a log file to store the path to the images with content
    # sampleid,0.0.0.0
    # paths to the images in s3 bucket 'bright-field-dev'
    # End
    # New line

    with open(f'/tmp/{sampleid}.log', 'a') as f:
        f.write(sampleid + '\n')
        for i in Path('/tmp/img/').glob('*.jpg'):
            f.write('s3://bright-field-dev/' + sampleid + '/' + i.name + '\n')
        f.write('End\n\n')

    # Upload log file to s3 bucket 'moichor-intermediate' with path 'receiver/new/'
    s3.upload_file(f'/tmp/{sampleid}.log', 'moichor-intermediate', f'receiver/new/{sampleid}.log')

    print('done')

    return {
        'statusCode': 200,
        'body': json.dumps('Success')
    }
