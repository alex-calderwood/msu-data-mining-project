import edu.stanford.nlp.hcoref.CorefCoreAnnotations.*;
import edu.stanford.nlp.hcoref.data.CorefChain;
import edu.stanford.nlp.hcoref.data.CorefChain.CorefMention;
import edu.stanford.nlp.ling.CoreAnnotations;
import edu.stanford.nlp.ling.CoreAnnotations.*;
import edu.stanford.nlp.ling.CoreLabel;
import edu.stanford.nlp.pipeline.Annotation;
import edu.stanford.nlp.pipeline.StanfordCoreNLP;
import edu.stanford.nlp.semgraph.SemanticGraph;
import edu.stanford.nlp.semgraph.SemanticGraphCoreAnnotations.*;
import edu.stanford.nlp.trees.Tree;
import edu.stanford.nlp.trees.TreeCoreAnnotations;
import edu.stanford.nlp.util.CoreMap;
import org.w3c.dom.Document;
import org.w3c.dom.Element;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import javax.xml.transform.OutputKeys;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerException;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;
import java.io.*;
import java.util.*;

import org.apache.commons.io.FilenameUtils;

/**
 * Created by Alex on 7/7/2016.
 */

public class Wrapper {
    StanfordCoreNLP pipeline;


    public Wrapper() {
        init();

//        File[] files = getFiles();
//
//        for (File file : files) {
//            String fileText = getTextFromFiles(file);
//            parse(file.getName(), fileText);
//        }

        easyParse("Here is some text to parse.");

    }

    private File[] getFiles() {
        String fileName = "TextFiles/";
        File folder = new File(fileName);
        System.out.println("File " + fileName + " exists " + folder.isDirectory());
        return folder.listFiles();
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
            System.out.println(
                    "Unable to open file '" +
                            file + "'");
        } catch (IOException ex) {
            System.out.println(
                    "Error reading file '"
                            + file + "'");
        }
        fileText = sb.toString();

        return fileText;
    }

    private void init() {
        // creates a StanfordCoreNLP object, with POS tagging, lemmatization, NER, parsing, and coreference resolution
        Properties props = new Properties();
        props.setProperty("annotators", "tokenize, ssplit, pos, lemma, ner, parse, dcoref, depparse");
        pipeline = new StanfordCoreNLP(props);
    }

    private void easyParse(String text) {
        // create an empty Annotation just with the given text
        Annotation document = new Annotation(text);

        // run all Annotators on this text
        pipeline.annotate(document);

        printTokenAnnotations(document);

        pr(text.toString() + "\n");
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

        System.out.println("Noun Phrases:");
        for (Tree NP : nouns) {
            System.out.println(NP.toString());
        }
        System.out.println();
    }

    private void printTokenAnnotations(Annotation document) {
        List<CoreMap> sentences = document.get(SentencesAnnotation.class);

        for(CoreMap sentence: sentences) {
            System.out.println("---Dependencies---");
            printDependencies(sentence);


            // traversing the words in the current sentence
            // a CoreLabel is a CoreMap with additional token-specific methods
            List<CoreLabel> tokens = sentence.get(TokensAnnotation.class);
            for (CoreLabel token : tokens) {

                String word = token.get(TextAnnotation.class);
                String pos = token.get(PartOfSpeechAnnotation.class);
                String ne = token.get(NamedEntityTagAnnotation.class);

                int index = token.index();

//                String depparse = token.get(BasicDependencyAnnotation.class);
                List bag = token.get(CoreAnnotations.BagOfWordsAnnotation.class);

                System.out.println(bag + " " + ne + " " + pos + "\t" + word + "\t" + index);
            }
        }
    }

    private void printDependencies(CoreMap sentence) {
        // this is the Stanford dependency graph of the current sentence
        SemanticGraph dependencies = sentence.get(CollapsedCCProcessedDependenciesAnnotation.class);

        System.out.println("Dependencies:");
        System.out.println(dependencies);
        System.out.println();
    }

    private void prln() {
        pr("\n");
    }

    private void pr(String text) {
        FileWriter fileWriter = null;
        try {
            fileWriter = new FileWriter("parseOutput.csv");
            fileWriter.append(text + "\t");
            System.out.print(text);
        } catch(IOException e) {
            System.out.println("Error Writing File");
            e.printStackTrace();
        } finally {
            try {
            fileWriter.flush();
            fileWriter.close();
            } catch (IOException e) {
                System.out.println("Error while closing File Writer");
                e.printStackTrace();
            }
        }
    }
    public static void main(String[] args) {
        new Wrapper();
    }
}