import libpybpe as bpe
import typing
import logging
import coloredlogs

from typing import Text

logger = logging.getLogger(__name__)
coloredlogs.install(level='INFO',
                    logger=logger,
                    fmt='%(asctime)s %(levelname)-8s %(name)s  - %(message)s')


class pyBPE:

    @staticmethod
    def create_vocab_file(text: Text, output_path: Text) -> None:
        try:
            vocab = bpe.get_vocabs(text)

            # to write to file sorted by frequency
            v = sorted(vocab.items(), key=lambda x: x[1], reverse=True)
            with open(output_path, 'w') as f:
                for tup in v:
                    f.write("{} {}\n".format(*tup))

        except Exception as e:
            logger.error("Unknown error while creating vocab file: {}".format(e))
            logger.exception(e)

    @staticmethod
    def create_bpe_file(text: Text, n_codes: int, output_path: Text) -> None:
        try:
            # learn bpe codes
            codes = bpe.learn_bpes(n_codes, text)

            # to write to file
            with open(output_path, 'w') as f:
                for tup in codes:
                    f.write("{} {} {}\n".format(*tup))

        except Exception as e:
            logger.error("Unknown error while creating BPE codes file: {}".format(e))
            logger.exception(e)

    @staticmethod
    def apply_bpe(text: Text, codes_path: Text, vocab_path: Text) -> Text:
        try:
            return bpe.apply_bpes(text, codes_path, vocab_path)
        except Exception as e:
            logger.error("Unknown error while applying BPE codes file: {}".format(e))
            logger.exception(e)
