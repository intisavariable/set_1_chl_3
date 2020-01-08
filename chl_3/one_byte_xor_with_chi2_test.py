import binascii

english_freq = [
    0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015,  
    0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749,  
    0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758, 
    0.00978, 0.02360, 0.00150, 0.01974, 0.00074  
]

def getChi2 (inpt):
    count = []
    ignored = 0
    for i in range(26):
        count.append(0)
    for char in inpt:
        c = ord(char)
        if c >= 65 and c <= 90:# uppercase A-Z 
            count[c - 65] += 1
            print(chr(c))
        elif c >= 97 and c <= 122:
            count[c-97] += 1  # lowercase a-z
            print(chr(c))
        elif c >= 32 and c<=126:
            ignored += 1  # numbers and punct.
        elif c == 9 or c == 10 or c == 13:
            ignored += 1   # TAB, CR, LF  
        else:
            return False
    
    chi2 = 0
    length = len(inpt) - ignored;
    for i in range(26):
        observed = count[i] 
        expected = length * english_freq[i]
        difference = observed - expected
        chi2 += difference * difference / expected;
    return chi2

class Result:
    def __init__(self, xor_key, decoded_text, chi2score):
        self.xor_key = xor_key
        self.decoded_text = decoded_text
        self.chi2score = chi2score
    def __repr__(self):
        return repr((self.xor_key, self.decoded_text, self.chi2score))


def main():
    encoded = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'


    nums = binascii.unhexlify(encoded)
    result_objects = []
    for xor_key in range(256):
        decoded = ''.join(chr(b ^ xor_key) for b in nums)
        result_objects.append(Result(xor_key, decoded, getChi2(decoded)))
        #if decoded.isprintable():
            
            #print(xor_key, decoded, getChi2(decoded))
    
    #result_objects.sort(key=lambda result: result.chi2score)
    for val in result_objects:
        if val.chi2score != False:
            print(val)
            print("\n")
    #print(sorted(result_objects, key=lambda result: result.chi2score))
    
if __name__ == "__main__":
    main()