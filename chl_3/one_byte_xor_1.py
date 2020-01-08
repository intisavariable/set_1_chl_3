encoded = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'
import binascii

nums = binascii.unhexlify(encoded)
key = max(nums, key=nums.count) ^ ord(' ')
print(''.join(chr(num ^ key) for num in nums))