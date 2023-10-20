Note: THIS REPOSITORY WAS SUPPOSED TO CONTAIN A DATABASE SUBDIVIDED INTO 43 SUBREPOSITORIES, REPRESENTING THE DATAS THE SCRIPT SHOULD HAVE WORKED WITH. HOWEVER, DUE TO THE DIMENSION OF THIS DATABASE, I WAS NOT ABLE TO UPLOAD IT. NEVERTHELESS I HAVE INCLUDED THE LINK AT THE YOUTUBE VIDEO SHOWCASING ITS OUTPOUT IN THE MAIN README FILE.

In my project, I started by building a basic model. It was designed to process images. The first model included:

- Convolution Layer: It had 32 filters with a 3x3 grid size (also known as kernel). I also used a function called ReLU for this layer. The shape of the input was set to IMG_WIDTH, IMG_HEIGHT, 3.
- MaxPooling Layer: This layer was 2x2 in size.
- Flatten Layer: This layer was used to turn the input into a flat array.
- Hidden Layer: This layer used the ReLU function, just like the Convolution Layer. It also had a dropout of 0.5, which is a technique to avoid overfitting.
- Output Layer: This layer used a function called SoftMax and had NUM_CATEGORIES nodes.

The first model didn't work too well. It only had an accuracy of 5% and the loss was 3.4953.
I therefore made some changes to improve the model: I added another pair of Convolution and MaxPooling layers and I also made the filters and pool size larger. Now, the model looked like this:

1. First Stage:
- Convolution Layer: 32 filters with a 4x4 grid and ReLU function.
- MaxPooling Layer: Pool size of 3x3.
2. Second Stage:
- Convolution Layer: 32 filters with a 3x3 grid and ReLU function.
- MaxPooling Layer: Pool size of 2x2.
The other parts of the model remained unchanged. 

These changes made a big difference. The accuracy went up to 89% and the loss went down to 0.3763.

The experimentation continued, exploring different activation functions like "Sigmoid" and "Softmax", but it became clear that the best fit was "ReLU" for hidden layers and "Softmax" for the final output layer. Moreover, adding more hidden layers and increasing the number of nodes didn't yield the expected results, resulting in decreased average accuracy and loss. So, I decided to reduce the dropout in the hidden layers from 0.5 to 0.1 and 0.05.

Finally, the best version of my model was:

1. Input Stages: These didn't change.
2. First Hidden Layer: It had NUM_CATEGORIES * 2 nodes, used ReLU function, and a dropout of 0.1.
3. Second Hidden Layer: It had NUM_CATEGORIES * 1.5 nodes, used ReLU function, and a dropout of 0.05.
4. Output Layer: It had NUM_CATEGORIES nodes and used SoftMax function.

This final version of the model was the best. It had an average accuracy of 94% and an average loss of 0.2127.