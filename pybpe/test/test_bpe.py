import pytest
import os


@pytest.mark.parametrize('vocab_file', ['/tmp/vocab'])
def test_read_vocab(bpe, vocab_file):
    vocab = bpe.read_vocab_file(vocab_file)
    print("Vocab from file: {}".format(vocab))
    assert all(isinstance(k, str) for k in vocab.keys())
    assert all(isinstance(v, int) for v in vocab.values())


@pytest.mark.parametrize('codes_file', ['/tmp/codes'])
def test_read_codes(bpe, codes_file):
    codes, reverse_codes = bpe.read_bpe_file(codes_file)
    print("Codes: {}".format(codes))
    print("Reverse codes: {}".format(reverse_codes))
    assert all(isinstance(k, tuple) for k in codes.keys())
    assert all(isinstance(v, int) for v in codes.values())
    assert all(isinstance(k, str) for k in reverse_codes.keys())
    assert all(isinstance(v, tuple) for v in reverse_codes.values())


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
