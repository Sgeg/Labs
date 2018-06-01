import java.math.BigInteger;
import java.io.Serializable;
import java.util.ArrayList;

class SearchConfig implements Serializable{
    public int num_to_test;
    public BigInteger bottom;
    public BigInteger top;
    public SearchConfig(int num_to_test, BigInteger bottom, BigInteger top){
        this.num_to_test = num_to_test;
        this.bottom = bottom;
        this.top = top;
    }
    public ArrayList<SearchConfig> split(int n){
        ArrayList<SearchConfig> configs = new ArrayList<SearchConfig>();
        for(int i = 0; i < n; ++i){
            configs.add(new SearchConfig(num_to_test / n, this.bottom, this.top));
        }
        return configs;
    }
}