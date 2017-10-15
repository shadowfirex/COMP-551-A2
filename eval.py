from sklearn.model_selection import cross_val_score, KFold
from sklearn.utils import shuffle
from sklearn.metrics import make_scorer, accuracy_score, precision_recall_fscore_support
import numpy as np

from linear.NB import NaiveBayes

# .... import a bunch of models here...


def PCA(X, n_component):
    C = np.cov(X.T)
    eig_val_cov, eig_vec_cov = np.linalg.eig(C)
    eig_pairs = [(np.abs(eig_val_cov[i]), eig_vec_cov[:,i]) for i in range(len(eig_val_cov))]
    eig_pairs.sort(key=lambda x: x[0], reverse=True)
    eig_vec = [p[1] for p in eig_pairs] ## sorted eigen_vec
    V = np.stack(eig_vec,axis=1)
    w = X.dot(V[:n_component].T)
    return w


def evaluate(models):
    X = np.load("preprocess/X.npy")
    y = np.load("preprocess/Y.npy").astype(int)
    # print(X.shape)
    # print(y.shape)
    X, y = shuffle(X,y.reshape((-1,)))
    acc_scorer = make_scorer(accuracy_score)

    kf = KFold(n_splits=10)
    for model in models:
        acc_avg = []
        f1_0_avg = []
        f1_1_avg = []
        for train_index, test_index in kf.split(X):
            X_train, X_valid = X[train_index], X[test_index]
            y_train, y_valid = y[train_index], y[test_index]
            model.fit(X_train, y_train)

            yp_valid = model.predict(X_valid)
            precision, recall, f1, _ = precision_recall_fscore_support(y_valid, yp_valid)
            acc = accuracy_score(y_valid, yp_valid)
          
            acc_avg.append(acc)
            f1_0_avg.append(f1[0])
            f1_1_avg.append(f1[1])
   
        print("accuracy mean",np.mean(np.array(acc_avg)))

    

if __name__ == "__main__":
    clf = [NaiveBayes(smoothing = 1)]
    evaluate(clf)
