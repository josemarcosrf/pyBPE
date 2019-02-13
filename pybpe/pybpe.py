import os
import sys
import typing
import logging
import coloredlogs

from typing import Text, List, Tuple, Dict

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import libpybpe as bpe

logger = logging.getLogger(__name__)
coloredlogs.install(level='INFO',
                    logger=logger,
                    fmt='%(asctime)s %(levelname)-8s %(name)s  - %(message)s')

class pyBPE:

    @staticmethod
    def get_vocab(text: Text) -> List[Tuple[Text, int]]:
        try:
            return bpe.get_vocabs(text)
        except Exception as e:
            logger.error("Unknown error while computing vocab: {}".format(e))
            logger.exception(e)

    @staticmethod
    def get_bpe_codes(text: Text, n_codes: int) -> List[Tuple[Text, Text, int]]:
        try:
            codes = bpe.learn_bpes(n_codes, text)
            # for sufficiently enough large values of 'n_codes'
            # 'learn_bpes' can return codes with count = 0
            # in those cases we filter the result before returning
            try:
                lim = [c[2] for c in codes].index(0)
                return codes[:lim]
            except ValueError:
                return codes

        except Exception as e:
            logger.error("Unknown error while computing BPE codes: {}".format(e))
            logger.exception(e)

    @staticmethod
    def create_vocab_file(text: Text, output_path: Text) -> None:
        vocab = pyBPE.get_vocab(text)
        pyBPE.write_vocab_file(vocab, output_path)

    @staticmethod
    def create_bpe_file(text: Text, n_codes: int, output_path: Text) -> None:
        codes = pyBPE.get_bpe_codes(text, n_codes)
        pyBPE.write_codes_file(codes, output_path)

    @staticmethod
    def apply_bpe(text: Text, codes_path: Text, vocab_path: Text) -> Text:
        try:
            return bpe.apply_bpes(text, codes_path, vocab_path)
        except Exception as e:
            logger.error("Unknown error while applying BPE codes file: {}".format(e))
            logger.exception(e)

    @staticmethod
    def write_vocab_file(vocab: Dict[Text, int],
                         output_path: Text) -> None:
        try:
            # write to file sorted by frequency
            v = sorted(vocab.items(), key=lambda x: x[1], reverse=True)
            with open(output_path, 'w') as f:
                for tup in v:
                    f.write("{} {}\n".format(*tup))

        except Exception as e:
            logger.error("Unknown error while creating vocab file: {}".format(e))
            logger.exception(e)

    @staticmethod
    def write_codes_file(codes: List[Tuple[Text, Text, int]],
                         output_path: Text) -> None:
        try:
            # write to file
            with open(output_path, 'w') as f:
                for tup in codes:
                    f.write("{} {} {}\n".format(*tup))

        except Exception as e:
            logger.error("Unknown error while creating BPE codes file: {}".format(e))
            logger.exception(e)
