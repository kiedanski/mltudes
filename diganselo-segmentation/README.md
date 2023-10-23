# Díganselo Segmentation

This étude was inspired by [El Kuelge's Díganselo videoclip](https://www.youtube.com/watch?v=Qy7LcH7pWZo). In it, we can see the camera following someone riding a bicycle through Buenos Aires.

In the rider t-shirt we can see several videos playing as if the t-shirt was some sort of TV. 

I quickly realized that I could achieve something similar by using a segmentation model to find a mask of the t-shirt and then overlapping that with another video.

I thought about using a pure CV model to segment t-shirts, but I quickly realized that it might take me a while to gather a dataset to fine-tune a segmentation model on t-shirts. Instead, I went for a multi-modal LLM that performed decently in a zero-shot setting.

 - [Video of man walking](https://www.pexels.com/video/a-man-walking-with-a-basketball-5192149/)
 - [Beach video](https://www.pexels.com/video/waves-rushing-and-splashing-to-the-shore-1409899/)