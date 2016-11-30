import edu.stanford.nlp.ie.util.RelationTriple;
import edu.stanford.nlp.ling.CoreAnnotations;
import edu.stanford.nlp.ling.CoreAnnotations.*;
import edu.stanford.nlp.ling.CoreLabel;
import edu.stanford.nlp.ling.IndexedWord;
import edu.stanford.nlp.naturalli.NaturalLogicAnnotations;
import edu.stanford.nlp.pipeline.Annotation;
import edu.stanford.nlp.pipeline.StanfordCoreNLP;
import edu.stanford.nlp.semgraph.SemanticGraph;
import edu.stanford.nlp.semgraph.SemanticGraphCoreAnnotations.*;
import edu.stanford.nlp.semgraph.semgrex.SemgrexMatcher;
import edu.stanford.nlp.semgraph.semgrex.SemgrexPattern;
import edu.stanford.nlp.sentiment.SentimentCoreAnnotations;
import edu.stanford.nlp.simple.Sentence;
import edu.stanford.nlp.trees.Tree;
import edu.stanford.nlp.trees.TreeCoreAnnotations;
import edu.stanford.nlp.util.CoreMap;

import java.io.*;
import java.util.*;

/**
 * Created by Alex on 7/7/2016.
 */

public class Wrapper {
    StanfordCoreNLP pipeline;

    // execution flags
    boolean runFullParse = true;
    boolean runSentiment = false;
    boolean runDepParse = false;
    boolean runTokenAnnotations = true;
    boolean runOpenIE = true;

    public Wrapper() {
        init();

        easyParse("Jimmy fed Billy the dog. Billy sat in a large house before moving on. He is a large dog.");
    }

    private String getTextFromFiles(File file) {
        String fileText;
        StringBuilder sb = new StringBuilder();
        try {
            FileReader fileReader =
                    new FileReader(file);

            BufferedReader bufferedReader =
                    new BufferedReader(fileReader);

            String line;
            while ((line = bufferedReader.readLine()) != null) {
                sb.append(line);
            }

            bufferedReader.close();
        } catch (FileNotFoundException ex) {
            IoUtils.prln(
                    "Unable to open file '" +
                            file + "'");
        } catch (IOException ex) {
            IoUtils.prln(
                    "Error reading file '"
                            + file + "'");
        }
        fileText = sb.toString();

        return fileText;
    }

    private void init() {
        // creates a StanfordCoreNLP object
        Properties props = new Properties();

        StringBuilder propertiesSB = new StringBuilder();
        propertiesSB.append("tokenize, ssplit, pos, lemma, ner, depparse");
        if(runFullParse)
            propertiesSB.append(", parse, dcoref");
        if (runFullParse && runSentiment)
            propertiesSB.append(", sentiment");
        if(runOpenIE)
            propertiesSB.append(", natlog, openie");

        String propertiesString = propertiesSB.toString();

        props.setProperty("annotators", propertiesString);
        pipeline = new StanfordCoreNLP(props);
    }


    private void easyParse(String text) {
        IoUtils.pr(text.toString() + "\n");

        // create an empty Annotation just with the given text
        Annotation document = new Annotation(text);

        // run all Annotators on this text
        pipeline.annotate(document);

        // print annotations
        if(runFullParse)
            printFullParse(document);
        if(runDepParse)
            printDepParse(document);
        if(runTokenAnnotations)
            printTokenAnnotations(document);
        if(runSentiment)
            printSentiment(document);
        if(runOpenIE)
            printOpenIeSvoTriple(document);
    }

    private void printParseTree(CoreMap sentence) {
        List<Tree> nouns = new ArrayList<Tree>();

        // this is the parse tree of the current sentence
        Tree parse = sentence.get(TreeCoreAnnotations.TreeAnnotation.class);
        //Parse Tree Class: edu.stanford.nlp.trees.LabeledScoredTreeNode

        for(Tree subtree: parse) {
            String phrase = subtree.label().value();
            if (phrase.equals("NP")) {
                nouns.add(subtree);
            }
        }

        IoUtils.prln("Noun Phrases:");
        for (Tree NP : nouns) {
            IoUtils.prln(NP.toString());
        }
        IoUtils.prln();
    }

    private void printTokenAnnotations(Annotation document) {
        List<CoreMap> sentences = document.get(SentencesAnnotation.class);

        for(CoreMap sentence: sentences) {
            // traversing the words in the current sentence
            // a CoreLabel is a CoreMap with additional token-specific methods
            List<CoreLabel> tokens = sentence.get(TokensAnnotation.class);
            for (CoreLabel token : tokens) {

                String word = token.get(TextAnnotation.class);
                String pos = token.get(PartOfSpeechAnnotation.class);
                String ne = token.get(NamedEntityTagAnnotation.class);

                int index = token.index();

                List bag = token.get(CoreAnnotations.BagOfWordsAnnotation.class);

                IoUtils.prln(bag + " " + ne + " " + pos + "\t" + word + "\t" + index);
            }
        }
    }

    private void printFullParse(Annotation document) {
        List<CoreMap> sentences = document.get(SentencesAnnotation.class);

        IoUtils.prln("---Full Parse---");

        for(CoreMap sentence: sentences) {
            // this is the Stanford dependency graph of the current sentence
            SemanticGraph dependencies = sentence.get(CollapsedCCProcessedDependenciesAnnotation.class);
            IoUtils.prln(dependencies.toString());
        }

        IoUtils.prln("---End Full Parse---");
    }

    private void printDepParse(Annotation document) {
        List<CoreMap> sentences = document.get(SentencesAnnotation.class);

        IoUtils.prln("---Dependencies---");

        for(CoreMap sentence: sentences) {
            // this is the Stanford dependency graph of the current sentence
            SemanticGraph dependencies = sentence.get(BasicDependenciesAnnotation.class);
//            SemanticGraph dependencies2 = sentence.get(EnhancedDependenciesAnnotation.class);
//            SemanticGraph dependencies3 = sentence.get(EnhancedPlusPlusDependenciesAnnotation.class);
            IoUtils.prln(dependencies.toString());
        }

        IoUtils.prln("---End Dependencies---");
    }

    private void printSentiment(Annotation document) {
        List<CoreMap> sentences = document.get(SentencesAnnotation.class);

        IoUtils.prln("---Sentiment---");

        for(CoreMap sentence: sentences) {
            Tree sent = null;
            if(runSentiment)
                 sent = sentence.get(SentimentCoreAnnotations.SentimentAnnotatedTree.class);

            IoUtils.prln(sent.toString());
        }

        IoUtils.prln("---Sentiment---");
    }


    private void svo1() {
        SemgrexPattern pattern = SemgrexPattern.compile("{$}=root >/.subj(pass)?/ {}=subject >/.obj/ {}=object");
        SemgrexMatcher matcher = pattern.matcher(new Sentence("A cat is sitting on the table").dependencyGraph());
        while (matcher.find()) {
            IndexedWord root = matcher.getNode("root");
            IndexedWord subject = matcher.getNode("subject");
            IndexedWord object = matcher.getNode("object");
            System.err.println(root.word() + "(" + subject.word() + ", " + object.word());
        }
    }

    private void printOpenIeSvoTriple(Annotation document) {
        IoUtils.prln("--- Begin SVO ---");
        // Loop over sentences in the document
        for (CoreMap sentence : document.get(CoreAnnotations.SentencesAnnotation.class)) {
            // Get the OpenIE triples for the sentence
            Collection<RelationTriple> triples = sentence.get(NaturalLogicAnnotations.RelationTriplesAnnotation.class);
            // Print the triples
            for (RelationTriple triple : triples) {
                IoUtils.prln(triple.confidence + "\t" +
                        triple.subjectLemmaGloss() + "\t" +
                        triple.relationLemmaGloss() + "\t" +
                        triple.objectLemmaGloss());
            }
        }

        IoUtils.prln("--- End SVO ---");
    }

    public static void main(String[] args) {
        new Wrapper();
    }
}