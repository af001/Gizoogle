#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 22:54:13 2018

@author: devnet
"""

from google.cloud import videointelligence

class VideoIntelligence():
    
    '''
    # Instantiate a video client
    '''     
    def get_client(self):
        return videointelligence.VideoIntelligenceServiceClient()

    '''
    # Analyze a video and print the Google Video Intelligence API response
    '''
    def analyze_video(self, URL, client):
        """Detect labels given a file path."""
        features = [videointelligence.enums.Feature.LABEL_DETECTION]
    
        operation = client.annotate_video(URL, features=features)
        result = operation.result(timeout=3600)
    
        # Process video/segment level label annotations
        segment_labels = result.annotation_results[0].segment_label_annotations
        for i, segment_label in enumerate(segment_labels):
            print('Video label description: {}'.format(
                segment_label.entity.description))
            for category_entity in segment_label.category_entities:
                print('Label category description: {}'.format(
                    category_entity.description))
    
            for i, segment in enumerate(segment_label.segments):
                start_time = (segment.segment.start_time_offset.seconds +
                              segment.segment.start_time_offset.nanos / 1e9)
                end_time = (segment.segment.end_time_offset.seconds +
                            segment.segment.end_time_offset.nanos / 1e9)
                positions = '{}s to {}s'.format(start_time, end_time)
                confidence = segment.confidence
                print('Segment {}: {}'.format(i, positions))
                print('Confidence: {}'.format(confidence))
            print('')
    
        # Process shot level label annotations
        shot_labels = result.annotation_results[0].shot_label_annotations
        for i, shot_label in enumerate(shot_labels):
            print('Shot label description: {}'.format(
                shot_label.entity.description))
            for category_entity in shot_label.category_entities:
                print('Label category description: {}'.format(
                    category_entity.description))
    
            for i, shot in enumerate(shot_label.segments):
                start_time = (shot.segment.start_time_offset.seconds +
                              shot.segment.start_time_offset.nanos / 1e9)
                end_time = (shot.segment.end_time_offset.seconds +
                            shot.segment.end_time_offset.nanos / 1e9)
                positions = '{}s to {}s'.format(start_time, end_time)
                confidence = shot.confidence
                print('Segment {}: {}'.format(i, positions))
                print('Confidence: {}'.format(confidence))
            print('')
    
        # Process frame level label annotations
        frame_labels = result.annotation_results[0].frame_label_annotations
        for i, frame_label in enumerate(frame_labels):
            print('Frame label description: {}'.format(
                frame_label.entity.description))
            for category_entity in frame_label.category_entities:
                print('Label category description: {}'.format(
                    category_entity.description))
    
            # Each frame_label_annotation has many frames,
            # here we print information only about the first frame.
            frame = frame_label.frames[0]
            time_offset = frame.time_offset.seconds + frame.time_offset.nanos / 1e9
            print('First frame time offset: {}s'.format(time_offset))
            print('First frame confidence: {}'.format(frame.confidence))
            print('')
