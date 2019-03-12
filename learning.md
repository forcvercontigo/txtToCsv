https://hacks.mozilla.org/2017/11/a-journey-to-10-word-error-rate/


The network has five layers: the input is fed into three fully connected layers, followed by a bidirectional RNN layer, and finally a fully connected layer. The hidden fully connected layers use the ReLU activation. The RNN layer uses LSTM cells with tanh activation.

The output of the network is a matrix of character probabilities over time. In other words, for each time step the network outputs one probability for each character in the alphabet, which represents the likelihood of that character corresponding to what’s being said in the audio at that time.

The CTC loss function (PDF link) considers all alignments of the audio to the transcription at the same time, allowing us to maximize the probability of the correct transcription being predicted without worrying about alignment. Finally, we train using the Adam optimizer.

CTC:
http://www.cs.toronto.edu/~graves/icml_2006.pdf
The basic idea is to interpret
the network outputs as a probability distribution over
all possible label sequences, conditioned on a given input sequence. Given this distribution, an objective
function can be derived that directly maximises the
probabilities of the correct labellings. Since the objective function is differentiable, the network can then be
trained with standard backpropagation through time
This section describes the output representation that
allows a recurrent neural network to be used for CTC.
The crucial step is to transform the network outputs
into a conditional probability distribution over label
sequences. The network can then be used a classifier
by selecting the most probable labelling for a given
input sequence.

 If at time step 0 the letter “C” is the most likely, and at time step 1 the letter “A” is the most likely, and at time step 2 the letter “T” is the most likely, then the transcription given by the simplest possible decoder will be “CAT”. This strategy is called greedy decoding.
 WHY LANGUAGE MODEL
 This is a pretty good way of decoding the probabilities output by the model into a sequence of characters, but it has one major flaw: it only takes into account the output of the network, which means it only takes into account the information from audio. When the same audio has two equally likely transcriptions (think “new” vs “knew”, “pause” vs “paws”), the model can only guess at which one is correct. This is far from optimal: if the first four words in a sentence are “the cat has tiny”, we can be pretty sure that the fifth word will be “paws” rather than “pause”. Answering those types of questions is the job of a language model, and if we could integrate a language model into the decoding phase of our model, we could get way better results.
 
 Now we get to use information not just from audio but also from our language model to decide which transcription is more likely. The algorithm is described in this paper by Hannun et. al.
PAPER:
First-Pass Large Vocabulary Continuous Speech Recognition using Bi-Directional Recurrent DNNs
