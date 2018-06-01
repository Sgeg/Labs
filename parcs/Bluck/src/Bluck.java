import java.util.Scanner;
import java.util.List;
import java.util.ArrayList;
import java.io.File;
import java.math.BigInteger;
import java.io.IOException;
import java.io.FileNotFoundException;
import java.io.BufferedReader;
import java.io.FileReader;
import parcs.*;

public class Bluck {
    public static void main(String[] args) throws Exception {
        task curtask = new task();
        curtask.addJarFile("PrimesSearch.jar");
        SearchConfig conf = fromFile(curtask.findFile("input"));

        AMInfo info = new AMInfo(curtask, null);

        ArrayList<channel> cs = new ArrayList<channel>();
        for(SearchConfig config: conf.split(2)){
            point p = info.createPoint();
            channel c = p.createChannel();
            p.execute("PrimesSearch");
            c.write(config);
            cs.add(c);
        }

        System.out.println("Waiting for result...");
        for(channel c: cs){
            System.out.println("Result: " + c.readLong());
        }
        curtask.end();
    }

    public static SearchConfig fromFile(String filename) throws Exception {
        int num_to_test = 0;
        BigInteger bottom = new BigInteger("0");
        BigInteger top = new BigInteger("0");
        try {
            BufferedReader reader = new BufferedReader(new FileReader(filename));
            num_to_test = Integer.parseInt(reader.readLine());
            bottom = new BigInteger(reader.readLine());
            top = new BigInteger(reader.readLine());
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
        SearchConfig config = new SearchConfig(num_to_test, bottom, top);
        return config;
    }
}
