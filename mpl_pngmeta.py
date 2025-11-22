import numpy as np
import matplotlib.pyplot as plt
from PIL.PngImagePlugin import PngInfo

plt.plot(np.sin(np.linspace(0, 3.1416, 100)))
mimetype, text = "text/x-python", "np.sin(np.linspace(0, 3.1416, 100))"

# metadata method
plt.savefig("sin.tEXt.png", metadata={
    # "Software": None,  # remove default if wanted
    mimetype: text,  # makes a tEXt chunk
})

info = PngInfo()
info.add_text(mimetype, text, zip=True)
plt.savefig("sin.zTXt.png", pil_kwargs=dict(pnginfo=info))
