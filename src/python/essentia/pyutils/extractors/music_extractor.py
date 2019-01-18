# Copyright (C) 2006-2016  Music Technology Group - Universitat Pompeu Fabra
#
# This file is part of Essentia
#
# Essentia is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the Free
# Software Foundation (FSF), either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the Affero GNU General Public License
# version 3 along with this program. If not, see http://www.gnu.org/licenses/

from essentia.standard import MusicExtractor, YamlOutput
from argparse import ArgumentParser
import os
import sys


def music_extractor(audio_file, sig_file, profile=None, store_frames=False):
    if profile:
        extractor = MusicExtractor(profile=profile)
    else:
        extractor = MusicExtractor()

    try:
        poolStats, poolFrames = extractor(audio_file)

    except Exception:
        print("Error processing", audio_file, ":", sys.exc_info()[0])   
        raise

    folder = os.path.dirname(sig_file)

    if not os.path.exists(folder):
        os.makedirs(folder)
    elif os.path.isfile(folder):
        print("Cannot create directory %s" % folder)
        print("There exist a file with the same name. Aborting analysis.")
        sys.exit()

    output = YamlOutput(filename=sig_file+'.sig')
    output(poolStats)
    if store_frames:
        YamlOutput(filename=sig_file + '.frames.sig')(poolFrames)

    print('ok!')


if __name__ == '__main__':
    parser = ArgumentParser(description = """
Analyzes an audio file using MusicExtractor.
""")

    parser.add_argument('audio_file', help='audio file name')
    parser.add_argument('sig_file', help='sig file name')
    parser.add_argument('--profile', help='MusicExtractor profile', required=False)
    parser.add_argument('--store_frames', help='store frames data', action='store_true', required=False)
    args = parser.parse_args()

    music_extractor(args.audio_file, args.sig_file, profile=args.profile, store_frames=args.store_frames)
