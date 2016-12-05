import java.io.*;

/**
 * Created by pie_a on 11/30/2016.
 */
public class IoUtils {

    // Singleton for writing to a given file
    private static FileWriter fileWriter = null;
    private static String fileName = "output.txt";

    private static FileWriter getFileWriter() {
        if(fileWriter != null)
            return fileWriter;
        else try {
            fileWriter = new FileWriter(fileName);
        } catch (IOException e) {
            e.printStackTrace();
        }
        return fileWriter;
    }

    public static File[] getFiles(String dir) {
        File folder = new File(dir);
        System.out.println("Folder " + dir + " exists " + folder.isDirectory());
        return folder.listFiles();
    }

    public static String extractText(File file) {
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

    public static void openFile(String name) {
        fileName = name;

        // Invalidate filewriter
        fileWriter = null;
    }

    public static void closeFile() {
        if(getFileWriter() == null)
            return;

        try {
            getFileWriter().flush();
            getFileWriter().close();
        } catch (IOException e) {
            System.out.println("Error while closing File Writer");
            e.printStackTrace();
        }

        // Invalidate filewriter
        fileWriter = null;
    }
}
