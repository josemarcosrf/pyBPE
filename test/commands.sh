
# Test getvocab
./fast getvocabs "this is a sample simple test test"
echo "this is a sample simple test test" | ./fast getvocab -

# test learnbpe
./fast learnbpes 10 "this is a sample simple test test"
echo "this is a sample simple test test" | ./fast learnbpe 10 -
