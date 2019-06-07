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

    def __init__(self, vocab_path=None, codes_path=None):
        self.vocab_path = vocab_path
        self.codes_path = codes_path

    def read_vocab_file(self) -> Dict:
        if self.vocab_path is None:
            raise ValueError("Vocab need to first be loaded")
        return bpe.read_vocab_file(self.vocab_path)

    def read_bpe_file(self) -> Tuple[Dict, Dict]:
        if self.codes_path is None:
            raise ValueError("Codes need to first be loaded")
        codes, reverse_codes = bpe.read_codes_file(self.codes_path)
        return codes, reverse_codes

    def load(self):
        try:
            self.vocab = self.read_vocab_file()
            self.codes, _ = self.read_bpe_file()
        except Exception as e:
            logger.error("Error loading BPE codes and vocab!")
            logger.exception(e)

    def apply_bpe(self, text: Text) -> Text:
        if self.vocab is None or self.codes is None:
            raise ValueError("Vocab and Codes need to first be loaded")
        try:
            return bpe.apply_bpe(text, self.codes, self.vocab)
        except Exception as e:
            logger.error("Unknown error "
                         "while applying BPE codes: {}".format(e))
            logger.exception(e)

    def apply_bpe_from_files(text, codes_file, vocab_file):
        try:
            return bpe.apply_bpe_from_files(text, codes_file, vocab_file)
        except Exception as e:
            logger.error("Unknown error "
                         "while applying BPE codes: {}".format(e))
            logger.exception(e)

    @staticmethod
    def create_vocab_file(text: Text, output_path: Text) -> None:
        vocab = pyBPE._learn_vocab(text)
        pyBPE._write_vocab_file(vocab, output_path)

    @staticmethod
    def create_bpe_file(text: Text, n_codes: int, output_path: Text) -> None:
        codes = pyBPE._learn_bpe_codes(text, n_codes)
        pyBPE._write_codes_file(codes, output_path)

    def _learn_vocab(text: Text) -> List[Tuple[Text, int]]:
        try:
            return bpe.get_vocabs(text)
        except Exception as e:
            logger.error("Unknown error while computing vocab: {}".format(e))
            logger.exception(e)

    @staticmethod
    def _learn_bpe_codes(text: Text,
                         n_codes: int) -> List[Tuple[Text, Text, int]]:
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
            logger.error("Unknown error "
                         "while computing BPE codes: {}".format(e))
            logger.exception(e)

    @staticmethod
    def _write_vocab_file(vocab: Dict[Text, int],
                          output_path: Text) -> None:
        try:
            # write to file sorted by frequency
            v = sorted(vocab.items(), key=lambda x: x[1], reverse=True)
            with open(output_path, 'w') as f:
                for tup in v:
                    f.write("{} {}\n".format(*tup))

        except Exception as e:
            logger.error("Unknown error "
                         "while creating vocab file: {}".format(e))
            logger.exception(e)

    @staticmethod
    def _write_codes_file(codes: List[Tuple[Text, Text, int]],
                          output_path: Text) -> None:
        try:
            # write to file
            with open(output_path, 'w') as f:
                for tup in codes:
                    f.write("{} {} {}\n".format(*tup))

        except Exception as e:
            logger.error("Unknown error while "
                         "creating BPE codes file: {}".format(e))
            logger.exception(e)
