#include <iostream>
#include <stdio.h>
#include <gmp.h>
#include <string>
#include <mpi.h>
#include <ctime>
#include <chrono>
#include <vector>

using namespace std;

char* serialize(mpz_t nums[], int num_count, int num_len){
    char *res = new char[num_len * num_count + 1];
    for(int i = 0; i < num_count; ++i){
        char *num_s = mpz_get_str(NULL, 2, nums[i]);
        strcpy(res + i * num_len, num_s);
    }
    return res;
}

mpz_t* deserialize(char* str, int num_count, int num_len){
    mpz_t* nums = new mpz_t[num_count];
    for(int i = 0; i < num_count; ++i){
        mpz_init_set_str(nums[i], str + i * num_len, 2);
    }
    return nums;
}

bool is_prime(mpz_t num);

void my_next_prime(mpz_t rop, mpz_t num){
    for(; true; mpz_add_ui(num, num, 1)){
        if(is_prime(num)){
            mpz_set(rop, num);
            return;
        }
    }
}

vector<int> trial_div= {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97};

void reduce(mpz_t T, uint32_t R, mpz_t N, mpz_t Np) {
    mpz_t Tmod; mpz_init(Tmod); mpz_set(Tmod, T);
    mpz_t m; mpz_init(m); mpz_mul(m, Tmod, Np);
    mpz_t tmp; mpz_init(tmp); mpz_mul(tmp, m, N);
    mpz_t res; mpz_init(res); mpz_add(res, T, tmp);
    if (mpz_cmp(res, N) < 0)
        mpz_sub(res, res, N);
}

bool is_prime(mpz_t num){
    int n_it = 10;
    for(int i = 0; i < trial_div.size(); ++i){
        mpz_t tmp; mpz_init(tmp);
        mpz_fdiv_r_ui(tmp, num, trial_div[i]);
        if(!mpz_cmp_ui(tmp, 0))
            return false;
    }
    mpz_t a; mpz_init(a);
    mpz_t R; mpz_init(R);
    string str(mpz_get_str(NULL, 2, num));
    mpz_t tmp; mpz_init_set_str(tmp, "2", 10);
    mpz_pow_ui(R, tmp, str.length());
    mpz_t one; mpz_init_set_str(one, "1", 10);
    mpz_t d; mpz_init(d); mpz_sub(d, num, one);
    int s = 0;
    mpz_div(R, num, one);
    mpz_t inv_one; mpz_init(inv_one); mpz_sub(inv_one, num, one);
    mpz_t inv; mpz_init(inv); mpz_invert(inv, num, R);
    mpz_t Np; mpz_init(Np); mpz_sub(Np, R, inv);
    for (int i = 0; i < n_it; ++i){

        if ( !mpz_cmp(a, one) || !mpz_cmp(a, inv_one))
            continue;
        int j = 0;
        for (; j < s - 1; ++j) {
            mpz_mul(a, a, a);
            reduce(a, str.length(), num, Np);
            if (!mpz_cmp(a, one))
                return false;
            else if (!mpz_cmp(a, inv_one))
                break;
        }
        if (j == s - 1)
            return false;
    }
    return true;
}

void next_prime(mpz_t prime, mpz_t num){
    mpz_nextprime(prime, num);
}

int main()
{

    MPI_Init(NULL, NULL);

    // Get the number of processes
    int world_size;
    MPI_Comm_size(MPI_COMM_WORLD, &world_size);

    // Get the rank of the process
    int world_rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);

    chrono::high_resolution_clock::time_point start;
    if(world_rank == 0){
        start = std::chrono::system_clock::now();
    }
    const int num_len = 2000;
    const int num_count_all = 40 / world_size * world_size;
    const int num_count = num_count_all / world_size;

    mpz_t pr[num_count];
    for(int i = 0; i < num_count; ++i)
        mpz_init(pr[i]);

    gmp_randstate_t state;
    gmp_randinit_default(state);
    gmp_randseed_ui(state, time(0) + world_rank);
    mpz_urandomb(pr[0], state, num_len);
    next_prime(pr[0], pr[0]);
    for(int i = 1; i < num_count; ++i)
        next_prime(pr[i], pr[i - 1]);

    char *res = serialize(pr, num_count, num_len);
    for(int i = 0; i < num_count; ++i)
        mpz_clear(pr[i]);
    char *primes_s = NULL;
    if(world_rank == 0)
        primes_s = new char[num_len * num_count_all + 1];
    MPI_Gather(res, num_count * num_len, MPI_BYTE, primes_s, num_count * num_len, MPI_BYTE, 0, MPI_COMM_WORLD);
    if(world_rank == 0){
        mpz_t *primes = deserialize(primes_s, num_count_all, num_len);
//        for(int i = 0; i < num_count_all; ++i)
//            cout << primes[i];
    }
    if(world_rank == 0){
        auto end = chrono::high_resolution_clock::now();
        chrono::duration<double> time_span = chrono::duration_cast<chrono::duration<double>>(end - start);
        cout << time_span.count() << " seconds" << endl;
    }
    MPI_Finalize();
    return 0;
}
