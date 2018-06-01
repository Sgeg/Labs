import java.util.List;
import java.util.ArrayList;
import java.math.BigInteger;
import parcs.*;

public class PrimesSearch implements AM {
    RabinMiller rabin_miller = new RabinMiller();
    public void run(AMInfo info) {
        SearchConfig conf = (SearchConfig)info.parent.readObject();
        ArrayList<BigInteger> primes = this.rabin_miller.findPrimes(conf.num_to_test, conf.bottom, conf.top);
        try {
            Thread.sleep(1);
        } catch (InterruptedException e) {
            e.printStackTrace();
            return;
        }
        System.out.println(conf.num_to_test + " nums tested.");
        info.parent.write(primes);
    }
}
