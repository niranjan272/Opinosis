##program to create and train a tagger. To save time as now there is no need to train the tagger again and again...after evaluation the accuracy of the tagger is around 95%
##program to evaluate the tagger
#import nltk
#import pickle
#from nltk.corpus import treebank
#train_sents = treebank.tagged_sents()[:3000]
#tagger=nltk.data.load('POSTrainedTagger.pickle')
#tagger.evaluate(train_sents)

from nltk.tag.sequential import ClassifierBasedPOSTagger
from nltk.corpus import treebank
import pickle

train_sents = treebank.tagged_sents()
POSTrainedTagger = ClassifierBasedPOSTagger(train=train_sents)
f = open('/usr/share/nltk_data/POSTrainedTagger.pickle', 'w')
pickle.dump(POSTrainedTagger, f)
f.close()



#import pickle
#from nltk.tag import DefaultTagger
#from nltk.tag import UnigramTagger
#from nltk.corpus import treebank
#
##tagger1 = DefaultTagger('NN')
#train_sents = treebank.tagged_sents()[:3000]
#POSTrainedTagger = UnigramTagger(train_sents)
#f = open('/usr/share/nltk_data/POSTrainedTagger.pickle', 'w')
#pickle.dump(POSTrainedTagger, f)
#f.close()



