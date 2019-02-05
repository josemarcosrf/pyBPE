import pytest
import os


@pytest.mark.parametrize('vocab_file', ['/tmp/vocab'])
def test_vocab(bpe, train_text, vocab, vocab_file):
    bpe.create_vocab_file(train_text, vocab_file)
    with open(vocab_file, 'r') as f:
        t_vocab = f.read()

    assert os.path.exists(vocab_file)
    assert t_vocab == vocab


@pytest.mark.parametrize('code_file,n_codes', [('/tmp/codes', 10)])
def test_learn_bpe(bpe, train_text, codes, code_file, n_codes):
    bpe.create_bpe_file(train_text, n_codes, code_file)

    with open(code_file, 'r') as f:
        t_codes = f.read()

    assert os.path.exists(code_file)
    assert t_codes == codes


@pytest.mark.parametrize('code_file,vocab_file', [('/tmp/codes', '/tmp/vocab')])
def test_apply_bpe(bpe, output, test_text, code_file, vocab_file):
    res = bpe.apply_bpe(test_text, code_file, vocab_file)

    assert res == output
