import java.io.*;

/**
 * Created by pie_a on 11/30/2016.
 */
public class IoUtils {

    // Singleton for writing to a given file
    private static FileWriter fileWriter = null;

    private static FileWriter getFileWriter() {
        if(fileWriter != null)
            return fileWriter;
        else try {
            fileWriter = new FileWriter("output.csv");
        } catch (IOException e) {
            e.printStackTrace();
        }
        return fileWriter;
    }

    public static File[] getFiles() {
        String fileName = "TextFiles/";
        File folder = new File(fileName);
        System.out.println("File " + fileName + " exists " + folder.isDirectory());
        return folder.listFiles();
    }

    public static String getTextFromFiles(File file) {
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

        // Get rid of all the text other than the reddit post
//        System.out.println("Text: " + fileText);
//        fileText = fileText.replaceAll(ignorePattern, "");
//        fileText = fileText.replaceAll(ellipsis, ". ");
//        System.out.println("Regex: " + fileText);

        return fileText;
    }

    public static void prln(String text) {
        pr(text + "\n");
    }

    public static void prln() {
        pr("\n");
    }

    public static void pr(String text) {
        try {
            getFileWriter().append(text + "\t");
            System.out.print(text);
        } catch(IOException e) {
            System.out.println("Error Writing File");
            e.printStackTrace();
        } finally {
            try {
                getFileWriter().flush();
            } catch (IOException e) {
                System.out.println("Error while flushing file writer");
                e.printStackTrace();
            }
        }
    }

    public static void close() {
        try {
            getFileWriter().flush();
            getFileWriter().close();
        } catch (IOException e) {
            System.out.println("Error while closing File Writer");
            e.printStackTrace();
        }
    }
}
