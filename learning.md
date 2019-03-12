https://hacks.mozilla.org/2017/11/a-journey-to-10-word-error-rate/


The network has five layers: the input is fed into three fully connected layers, followed by a bidirectional RNN layer, and finally a fully connected layer. The hidden fully connected layers use the ReLU activation. The RNN layer uses LSTM cells with tanh activation.

The output of the network is a matrix of character probabilities over time. In other words, for each time step the network outputs one probability for each character in the alphabet, which represents the likelihood of that character corresponding to what’s being said in the audio at that time.

The CTC loss function (PDF link) considers all alignments of the audio to the transcription at the same time, allowing us to maximize the probability of the correct transcription being predicted without worrying about alignment. Finally, we train using the Adam optimizer.

