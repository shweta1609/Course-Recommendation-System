package com.bigdatasystems;

import edu.stanford.nlp.ling.CoreAnnotations;
import edu.stanford.nlp.neural.rnn.RNNCoreAnnotations;
import edu.stanford.nlp.pipeline.Annotation;
import edu.stanford.nlp.pipeline.StanfordCoreNLP;
import edu.stanford.nlp.sentiment.SentimentCoreAnnotations;
import edu.stanford.nlp.trees.Tree;
import edu.stanford.nlp.util.CoreMap;
import org.ejml.simple.SimpleMatrix;

import java.util.Properties;

public class SentimentAnalyzer {
    StanfordCoreNLP pipeline;

    public void initialize() {
        Properties properties = new Properties();
        properties.setProperty("annotators", "tokenize, ssplit, parse, sentiment");
        pipeline = new StanfordCoreNLP(properties);
    }

    public SentimentResult getSentimentResult(String text) {
        SentimentClassification classification = new SentimentClassification();
        SentimentResult sentimentResult = new SentimentResult();
        if (text != null && text.length() > 0) {
            Annotation annotation = pipeline.process(text);
            for(CoreMap sentence: annotation.get(CoreAnnotations.SentencesAnnotation.class)) {
                //System.out.println("Sentence: "+ sentence);
                Tree tree = sentence.get(SentimentCoreAnnotations.SentimentAnnotatedTree.class);
                //System.out.println("TREE" + tree);
                SimpleMatrix simpleMatrix = RNNCoreAnnotations.getPredictions(tree);
                //System.out.println("SimpleMatrix" + simpleMatrix);
                classification.setVeryNegative((int)Math.round(simpleMatrix.get(0)*100d));
                classification.setNegative((int)Math.round(simpleMatrix.get(1)*100d));
                classification.setNeutral((int)Math.round(simpleMatrix.get(2)*100d));
                classification.setPositive((int)Math.round(simpleMatrix.get(3)*100d));
                classification.setVeryPositive((int)Math.round(simpleMatrix.get(4)*100d));
                String sentimentType = sentence.get(SentimentCoreAnnotations.SentimentClass.class);
                sentimentResult.setSentimentType(sentimentType);
                sentimentResult.setSentimentClass(classification);
                sentimentResult.setSentimentScore(RNNCoreAnnotations.getPredictedClass(tree));
            }
        }
        return sentimentResult;
    }
}