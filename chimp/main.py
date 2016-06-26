"""
Chip-Hybridized Affinity Mapping Platform

Usage:
  champ map FASTQ_DIRECTORY OUTPUT_DIRECTORY PATHS_TO_BAMFILES ... [--force] [-v | -vv | -vvv]
  champ init MAPPED_READS IMAGE_DIRECTORY [--microns-per-pixel=0.266666666] [--chip=miseq] [--ports-on-right] [--flipud] [--fliplr] [-v | -vv | -vvv ]
  champ align ALIGNMENT_CHANNEL [--second-channel SECOND_CHANNEL_NAME] [--min-hits MIN_HITS] [--snr-threshold SNR] [--make-pdfs] [-v | -vv | -vvv]
  champ kd IMAGE_DIRECTORY PROCESSED_READS_DIRECTORY CHIP_NAME TARGET_DATA TARGET OFF_TARGET [-v | -vv | -vvv]
  champ info IMAGE_DIRECTORY [-v | -vv | -vvv]

Options:
  -h --help     Show this screen.
  --version     Show version.

Commands:
  map           Maps all the reads in the fastq files. This needs to be done before any other processing
  init          Configures and preprocesses a directory of image data for analysis
  align         Determines the sequence of fluorescent points in the microscope data
  kd            Determines boundaries of clusters, assigns intensities to sequences and derives the apparent Kd's
  info          brief summary of the data

"""
from chimp.controller import align, preprocess, mapreads, convert, intensity, info
from docopt import docopt
import logging
from chimp.config import CommandLineArguments
from chimp.constants import VERSION
import os


def main(**kwargs):
    dargs = docopt(__doc__, version=VERSION)
    arguments = CommandLineArguments(dargs, os.getcwd())

    log = logging.getLogger()
    log.addHandler(logging.StreamHandler())
    log.setLevel(arguments.log_level)
    log.debug(str(dargs))

    # make some space to distinguish log messages from command prompt
    for _ in range(2):
        log.info('')

    commands = {'align': align,
                'preprocess': preprocess,
                'map': mapreads,
                'convert': convert,
                'intensity': intensity,
                'info': info}

    commands[arguments.command].main(arguments)


if __name__ == '__main__':
    main()
