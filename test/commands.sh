
# Test getvocab
./fast getvocabs "this test is a simple sample test"
echo "this is a sample simple test test" | ./fast getvocab -

# test learnbpe
./fast learnbpes 10 "this test is a simple sample test"
echo "this is a sample simple test test" | ./fast learnbpe 10 -

# apply bpe with OOV words (i.e.: simplest, example)
./fast applybpes "this is the simplest example" codes vocab
./fast applybpe out.txt input.txt codes vocab
