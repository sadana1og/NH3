input = ["a","v","c","s","3"]
indices = list(range(len(input)))
indices.sort(key=lambda x: input[x])
output = [0] * len(indices)
for i, x in enumerate(indices):
	output[x] = i
	
input.sort(key=lambda r:r[0])
print(input)
for i in range(3):
	"asd"+i = i
	print("asd"+i)