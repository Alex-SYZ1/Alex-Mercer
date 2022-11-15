from PIL import Image
a="demo - 副本.jpg"
b=""
im=Image.open(a)
resizes_im=im.resize((160,80))
resizes_im=resizes_im.convert('RGB')
resizes_im.save(b+"demo.jpg")#,dpi=(70,70)
